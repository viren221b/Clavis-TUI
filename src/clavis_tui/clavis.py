from textual.app import App, ComposeResult
from textual.widgets import Label, Input, Button, ListView, ListItem, Footer, Header, Static, TextArea
from textual.containers import Vertical, Horizontal, ScrollableContainer
from textual.screen import Screen
from textual.binding import Binding

from clavis_tui.engine import vault_exists, create_vault, unlock_vault, add_entry, save_vault, save_theme, load_theme
from argon2.exceptions import VerifyMismatchError
from cryptography.fernet import Fernet


#MAINSCREEN
class MainScreen(Screen):

    BINDINGS = [
        Binding("a", "add_entry", "Add"),
        Binding("e", "edit_entry", "Edit"),
        Binding("d", "delete_entry", "Delete"),
        Binding("ctrl+f", "toggle_search", "Search"),
        Binding("q", "quit", "Quit")
    ]

    #possible changes:
        # - adjustable containers
    CSS = """
    #search_bar {
        display: none;
        height: 3;
        margin: 0 0;
    }

    Horizontal {
        height: 1fr;
    }

    #entry_list {
        width: 60%;
        height: 100%;
        padding: 1 1 1 1;
        scrollbar-size-vertical: 0;
    }

    #content_scroll {
        width: 40%;
        height: 100%;
        padding: 1 1 1 1;
        scrollbar-size-vertical: 0;
    }

    #entry_content {
        padding: 0 2 0 0;
    }
    """

    def __init__(self, fernet, vault_data):
        super().__init__()
        self.fernet = fernet
        self.vault_data = vault_data
        self.filtered_indices = []

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Input(placeholder="Search (ex: title, topic, content, date, or type)", id="search_bar")
        yield Horizontal(
            ListView(id="entry_list"),
            ScrollableContainer(
                Static("Select an entry to view it.", id="entry_content"),
                id="content_scroll",
                can_focus=True
            )
        )
        yield Footer()

    def on_mount(self) -> None:
        self.call_after_refresh(self.refresh_list)
        self.query_one("#entry_list", ListView).focus()

    def refresh_list(self):
        self.filter_list("")

    def on_key(self, event) -> None:
        if event.key == "escape":
            search_bar = self.query_one("#search_bar", Input)
            if search_bar.display:
                search_bar.display = False
                search_bar.value = ""
                self.filter_list("")

    def action_quit(self):
        self.app.exit()

    def action_edit_entry(self) -> None:
        index = self.query_one("#entry_list", ListView).index
        if index is None or index < 0:
            return
        self.app.push_screen(EditEntryScreen(self.fernet, self.vault_data, index))

    def action_delete_entry(self):
        index = self.query_one("#entry_list", ListView).index
        if index is None or index < 0:
            return
        self.app.push_screen(DeleteEntryScreen(self.fernet, self.vault_data, index))

    def action_toggle_search(self):
        search_bar = self.query_one("#search_bar", Input)
        search_bar.display = not search_bar.display
        if search_bar.display:
            search_bar.focus()
        else:
            search_bar.value = ""
            self.filter_list("")

    def on_input_changed(self, event: Input.Changed) -> None:
        if event.input.id == "search_bar":
            self.filter_list(event.value)

    def filter_list(self, term: str) -> None:
        entry_list = self.query_one("#entry_list", ListView)
        entry_list.clear()
        self.filtered_indices = []
        term = term.lower().strip()
        for i, entry in enumerate(self.vault_data["entries"]):
            title = self.fernet.decrypt(entry["title"].encode()).decode()
            topic = self.fernet.decrypt(entry["topic"].encode()).decode()
            content = self.fernet.decrypt(entry["content"].encode()).decode()
            date = self.fernet.decrypt(entry["date"].encode()).decode()
            entry_type = entry["type"]
            if not term or term in title.lower() or term in topic.lower() or term in content.lower() or term in date.lower() or term in entry_type.lower():
                self.filtered_indices.append(i)
                entry_list.append(ListItem(Label(f"[{entry_type}] {title} - {topic}")))

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        list_index = event.list_view.index
        actual_index = self.filtered_indices[list_index]
        entry = self.vault_data["entries"][actual_index]
        title = self.fernet.decrypt(entry["title"].encode()).decode()
        date = self.fernet.decrypt(entry["date"].encode()).decode()
        topic = self.fernet.decrypt(entry["topic"].encode()).decode()
        content = self.fernet.decrypt(entry["content"].encode()).decode()
        self.query_one("#entry_content").update(
            f"[{entry['type']}] {title}\n{date} -- {topic}\n\n{content}"
        )

    def action_add_entry(self) -> None:
        self.app.push_screen(AddEntryScreen(self.fernet, self.vault_data))

    def on_screen_resume(self) -> None:
        self.refresh_list()


#EDIT ENTRY SCREEN
class EditEntryScreen(Screen):

    BINDINGS = [
        Binding("ctrl+w", "save", "Save", priority=True, show=True),
        Binding("escape", "cancel", "Cancel")
    ]

    CSS = """
    
    #edit_container Label {
        margin-bottom: 1;
        margin-top: 1;
    }

    #edit_container {
        width: 100%;
        height: 100%;
        padding: 0 2;
    }

    #edit_container Input {
        width: 100%;
        height: 3;
        margin-bottom: 1;
    }

    #edit_container TextArea {
        height: 1fr;
        margin-top: 1;
    }
    """

    def __init__(self, fernet, vault_data, index):
        super().__init__()
        self.fernet = fernet
        self.vault_data = vault_data
        self.index = index

    def compose(self) -> ComposeResult:
        entry = self.vault_data["entries"][self.index]
        title = self.fernet.decrypt(entry["title"].encode()).decode()
        topic = self.fernet.decrypt(entry["topic"].encode()).decode()
        entry_type = entry["type"]
        content = self.fernet.decrypt(entry["content"].encode()).decode()

        yield Header(show_clock=True)
        yield Vertical(
            Label("Edit Entry"),
            Input(value=title, placeholder="Title", id="title"),
            Input(value=topic, placeholder="Topic", id="topic"),
            Input(value=entry_type, placeholder="Type (ex. journal)", id="entry_type"),
            TextArea(content, id="content"),
            Static("", id="message"),
            id="edit_container"
        )
        yield Footer()

    def action_save(self) -> None:
       title = self.query_one("#title").value
       topic = self.query_one("#topic").value
       entry_type = self.query_one("#entry_type").value
       content = self.query_one("#content", TextArea).text

       if not title or not topic or not entry_type or not content:
           self.query_one("#message").update("All fields are required")
           return
       entry = self.vault_data["entries"][self.index]
       entry["title"] = self.fernet.encrypt(title.encode()).decode()
       entry["topic"] = self.fernet.encrypt(topic.encode()).decode()
       entry["type"] = entry_type
       entry["content"] = self.fernet.encrypt(content.encode()).decode()

       save_vault(self.vault_data)
       self.app.pop_screen()

    def action_cancel(self) -> None:
        self.app.pop_screen()


#DELETE ENTRY SCREEN
class DeleteEntryScreen(Screen):
    BINDINGS = [
        Binding("escape", "cancel", "Cancel")
    ]

    CSS = """
        DeleteEntryScreen {
            align: center middle;
        }

        #delete_container {
            width: 50;
            height: auto;
            padding: 2 4;
            border: round white;
        }

        #delete_container Label {
            width: 100%;
            margin-bottom: 1;
        }

        #delete_container Horizontal {
            height: auto;
            margin-top: 1;
        }

        #delete_container Button {
            width: 1fr;
            margin: 0 1;
        }
        """

    def __init__(self, fernet, vault_data,index):
        super().__init__()
        self.fernet = fernet
        self.vault_data = vault_data
        self.index = index

    def compose(self) -> ComposeResult:
        entry = self.vault_data["entries"][self.index]
        title = self.fernet.decrypt(entry["title"].encode()).decode()
        yield Header(show_clock=True)
        yield Vertical(
            Label(f"Delete '{title}'?"),
            Label("This cannot be undone."),
            Horizontal(
                Button("Delete", id="confirm_delete"),
                Button("Cancel", id="cancel")
            ),
            Static("", id="message"),
            id="delete_container"
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "confirm_delete":
            del self.vault_data["entries"][self.index]
            save_vault(self.vault_data)
            self.app.pop_screen()
        elif event.button.id == "cancel":
            self.action_cancel()

    def action_cancel(self) -> None:
        self.app.pop_screen()


#ADD ENTRY SCREEN
class AddEntryScreen(Screen):
    BINDINGS = [
        Binding("ctrl+w", "save", "Save", priority=True),
        Binding("escape", "cancel", "Cancel")
    ]

    CSS = """
        #add_container {
            width: 100%;
            height: 100%;
            padding: 0 2;
        }

        #add_container Label {
            margin-bottom: 1;
            margin-top: 1;
        }

        #add_container Input {
            width: 100%;
            height: 3;
            margin-bottom: 1;
        }

        #add_container TextArea {
            height: 1fr;
            margin-top: 1;
        }
        """

    def __init__(self, fernet, vault_data):
        super().__init__()
        self.fernet = fernet
        self.vault_data = vault_data

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Vertical(
            Label("New Entry"),
            Input(placeholder="Title", id="title"),
            Input(placeholder="Topic", id="topic"),
            Input(placeholder="Type (ex. journal)", id="entry_type"),
            TextArea(id="content"),
            Static("", id="message"),
            id="add_container"
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save":
            self.action_save()
        elif event.button.id == "cancel":
            self.action_cancel()

    def action_save(self) -> None:
        title = self.query_one("#title").value
        topic = self.query_one("#topic").value
        entry_type = self.query_one("#entry_type").value
        content = self.query_one("#content").text

        if not title or not topic or not entry_type or not content:
            self.query_one("#message").update("All fields are required.")
            return

        add_entry(self.fernet, self.vault_data, entry_type, title, topic, content)
        self.app.pop_screen()

    def action_cancel(self) -> None:
        self.app.pop_screen()

#CREATE VAULT SCREEN
class CreateVaultScreen(Screen):

    CSS = """
        CreateVaultScreen {
            align: center middle;
        }

        #vcreate_container {
            width: 60;
            height: auto;
            padding: 2 4;
            border: round white;
        }

        #vcreate_container Label {
            width: 100%;
            margin-bottom: 1;
        }

        #vcreate_container Input {
            width: 100%;
            margin-bottom: 1;
        }

        #vcreate_container Button {
            width: 100%;
            margin-top: 1;
        }
        """

    def compose(self) -> ComposeResult:
        yield Vertical(
            Label("welcome to clavis"),
            Label("No vault found. Create one to get started."),
            Input(placeholder="Master password", password=True, id="password"),
            Input(placeholder="Confirm password", password=True, id="confirm"),
            Button("Create Vault", id="create"),
            Static("", id="message"),
            id="vcreate_container"
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "create":
            password = self.query_one("#password").value
            confirm = self.query_one("#confirm").value

            if not password or not confirm:
                self.query_one("#message").update("Both fields are required")
                return
            if password != confirm:
                self.query_one("#message").update("Passwords do not match, try again.")
                return
            if len(password) < 8:
                self.query_one("#message").update("Password must be at least 8 characters")
                return

            create_vault(password)
            self.app.push_screen(AuthScreen())


#AUTHENTICATION SCREEN
class AuthScreen(Screen):

    CSS = """
        AuthScreen {
            align: center middle;
        }

        #auth_container {
            width: 60;
            height: auto;
            padding: 2 4;
            border: round white;
            scrollbar-size-vertical: 0;
        }

        #auth_container Label {
            width: 100%;
            margin-bottom: 1;
        }

        #auth_container Input {
            width: 100%;
            margin-bottom: 1;
        }

        #auth_container Button {
            width: 100%;
            margin-top: 1;
        }
        """

    def compose(self) -> ComposeResult:
        yield Vertical(
            Label("clavis", id="auth_title"),
            Label("Enter your master password"),
            Input(placeholder="Master password", password=True, id="password"),
            Button("Unlock", id="unlock"),
            Label("", id="message"),
            id="auth_container"
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "unlock":
            password = self.query_one("#password").value
            if not password:
                self.query_one("#message").update("Please enter a password")
                return
            try:
                key, vault_data = unlock_vault(password)
                fernet = Fernet(key)
                self.app.push_screen(MainScreen(fernet, vault_data))
            except VerifyMismatchError:
                self.query_one("#message").update("Wrong password. Try again")


#MAIN APPLICATION LOOP
class clavis(App):
    def on_mount(self) -> None:
        self.theme = load_theme()
        if vault_exists():
            self.push_screen(AuthScreen())
        else:
            self.push_screen(CreateVaultScreen())

    def on_theme_changed(self, event) -> None:
        save_theme(self.theme)


def main():
    app = clavis()
    app.run()

if __name__ == "__main__":
    main()

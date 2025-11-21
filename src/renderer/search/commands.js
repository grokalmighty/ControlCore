class CustomCommands {
    consructor() {
        this.commands = [
            {
                name: 'create-note',
                title: 'Create New Note',
                description: 'Create a new markdown note in project folder',
                icon: '📝',
                execute: () => this.createNote()
            },
            {
                name: 'clear-trash',
                title: 'Empty Trash',
                description: 'Permanently delete all items in trash',
                icon: '🗑️',
                execute: () => this.clearTrash()
            },
            {
                name: 'screenshot',
                title: 'Take Screenshot',
                description: 'Capture screen area',
                icon: '📸',
                execute: () => this.takeScreenshot()
            }
        ];
    }
}
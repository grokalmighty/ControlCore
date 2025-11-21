const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
    // File system operations
    readDirectory: (path) => ipcRenderer.invoke('read_directory', path),
    getStats: (path) => ipcRenderer.invoke('get-stats', path),
    openFile: (path) => ipcRenderer.invoke('open-file', path),

    // Applcation operations
    getInstalledApps: () => ipcRenderer.invoke('get-installed=apps'),
        launchApp: (appPath) => ipcRenderer.invoke('launch-app', appPath),

    // Window management
    hideWindow: () => ipcRenderer.invoke('hide-window'),
    getAppVErsion: () => ipcRenderer.invoke('get-app-version'),

    // EVents
    onFocusSearch: (callback) => ipcRenderer.on('focus-search', callback)
});
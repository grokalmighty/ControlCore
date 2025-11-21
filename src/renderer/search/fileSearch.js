class FileSearch {
    constructor () {
        this.index = [];
        this.isIndexing = false;
        this.startIndexing();
    }

    async startIndexing() {
        if (this.isIndexing) return;

        this.isIndexing = true;
        try {
            // Index common directories
            const homeDir = await window.electronAPI.getHomeDirectory();
            await this.indexDirectory(homeDir);
        } catch (error) {
            console.error('Indexing failed:', error);
        }
        this.isIndexing = false;
    }
}
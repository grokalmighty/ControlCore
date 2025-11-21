const fs = require('fs').promises;
const path = require('path');

class FileIndexer {
    constructor() {
        this.index = new Map();
        this.isIndexing = false;
        this.indexVersion = 1;
        this.supportedFileTypes = new Set([
            'txt', 'md', 'js', 'html', 'css', 'json', 'xml', 'csv',
            'pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 
            'jpg', 'jpeg', 'png', 'gif', 'svg', 'mp3', 'mp4', 'avi',
            'mov', 'wav', 'zip', 'rar', '7z'
        ]);
    }

    async initialize(userDataPath) {
        this.indexPath = path.join(userDataPath, 'search-index.json');
        await this.loadIndex();
    }
}
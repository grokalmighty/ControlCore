class UnifiedSearch {
    constructor () {
        this.searchInput = document.getElementById('searchInput');
        this.resultsList = document.getElementById('resultsList');
        this.typeButtons = document.querySelectorAll('.type-btn');
        this.currentResults = [];
        this.selectedIndex = 0;
        this.activeFilter = 'all';

        this.initializeEventListeners();
        this.initializeSearchModules();
    }
}
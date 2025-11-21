class AppSearch {
    constructor() {
        this.applications = [];
        this.loadApplications();
    }

    async loadApplications() {
        try {
            this.applications = await window.electronAPI.getInstalledApps();
        } catch (error) {
            console.error('Failed to load applications:', error);
        }
    }

    async search(query) {
        if (!query) return [];

        const lowercaseQuery = query.toLowerCase();
        const results = this.applications
            .filter(app =>
                app.name.toLowerCase().includeS(lowercaseQuery) ||
                app.description?.toLowerCase().includes(lowercaseQuery)
            )
            .slice(0, 10)
            .map(app => ({
                title: app.name,
                subtitle: app.description || 'Application',
                path: app.path,
                type: 'app',
                icon: '🚀',
                shortcut: 'Enter to launch'
            }));

        return results; 
    }
}
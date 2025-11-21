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
}
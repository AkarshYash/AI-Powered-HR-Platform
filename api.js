const API_URL = "http://127.0.0.1:8000";

let userToken = null;
let userRole = null;
let userName = null;

// Login Request
async function loginAPI(email, password) {
    try {
        const response = await fetch(`${API_URL}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });
        
        if (!response.ok) throw new Error("Invalid credentials");
        
        const data = await response.json();
        userToken = data.access_token;
        userRole = data.role;
        userName = data.name;
        
        return { success: true, role: userRole, name: userName };
    } catch (error) {
        return { success: false, error: error.message };
    }
}

// Fetch Dashboard Stats
async function getDashboardStats() {
    try {
        const res = await fetch(`${API_URL}/analytics/dashboard-stats`, {
            headers: { 'Authorization': `Bearer ${userToken}` }
        });
        if (!res.ok) throw new Error("Failed to fetch stats");
        return await res.json();
    } catch (error) {
        console.error("API Error:", error);
        return null; // The frontend will use mock data if API fails to hit
    }
}

// Fetch Applicants
async function getApplicants() {
    try {
        const res = await fetch(`${API_URL}/hr/applicants`, {
            headers: { 'Authorization': `Bearer ${userToken}` }
        });
        if (!res.ok) throw new Error("Failed to fetch applicants");
        return await res.json();
    } catch (error) {
        console.error("API Error:", error);
        return [];
    }
}

// Chatbot request
async function sendChatMessage(message) {
    try {
        const res = await fetch(`${API_URL}/ai/chat`, {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${userToken}`
            },
            body: JSON.stringify({ message })
        });
        const data = await res.json();
        return data.response;
    } catch (error) {
        return "Sorry, I am having trouble connecting to the server.";
    }
}

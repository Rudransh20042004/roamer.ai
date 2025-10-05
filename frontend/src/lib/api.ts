const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

export async function getData(coords: { lat: number; lng: number }) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/tour-guide`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                lat: coords.lat,
                lng: coords.lng
            })
        });

        if (!response.ok) {
            throw new Error('Failed to fetch tour data');
        }

        const data = await response.json();
        
        // Convert base64 audio to blob URL
        const audioBlob = new Blob([
            Uint8Array.from(atob(data.audio), c => c.charCodeAt(0))
        ], { type: 'audio/mpeg' });
        const voiceUrl = URL.createObjectURL(audioBlob);

        return {
            imageUrl: "https://www.tclf.org/sites/default/files/thumbnails/image/HarvardUniversity-sig.jpg",
            voiceUrl: voiceUrl,
            description: data.description
        };
    } catch (error) {
        console.error('Error fetching tour data:', error);
        // Fallback to placeholder data
        return {
            imageUrl: "https://www.tclf.org/sites/default/files/thumbnails/image/HarvardUniversity-sig.jpg",
            voiceUrl: "https://github.com/rafaelreis-hotmart/Audio-Sample-files/raw/master/sample.mp3",
            description: "Welcome to your location-based tour guide!"
        };
    }
}
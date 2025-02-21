import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL;

export async function getComments(sentiment) {
    try {
        const params = sentiment ? { sentiment } : {};
        const response = await axios.get(`${API_URL}/comments`, { params });
        return response.data;
    } catch (error) {
        console.error('Error fetching comments:', error);
        throw error;
    }
}

import axios from 'axios';

const api = axios.create({
	baseURL: 'http://localhost:3000/api', // Replace with your backend URL
});

export default api;

export async function getProductById(id: string) {
	try {
		const response = await axios.get(`/api/products/${id}`);
		return response.data;
	} catch (error) {
		console.error('Error fetching product:', error);
		return null;
	}
}

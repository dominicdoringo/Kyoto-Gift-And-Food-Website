import axios from 'axios';
import { Product } from '@/lib/types';

const api = axios.create({
	baseURL: 'http://localhost:8000/api', // Replace with your backend URL
});

export default api;

export async function getProductById(id: string) {
	try {
		const response = await api.get<Product>(`/products/${id}`);
		return response.data;
	} catch (error) {
		console.error('Error fetching product:', error);
		return null;
	}
}

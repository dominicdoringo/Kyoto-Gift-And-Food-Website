import axios from 'axios';
import { Product } from '@/lib/types';
import { API_HOST_BASE_URL } from '@/lib/constants';

const api = axios.create({
	baseURL: API_HOST_BASE_URL, // Replace with your backend URL
});

export default api;

export async function getProductById(id: number) {
	try {
		const response = await api.get<Product>(`/products/${id}`);
		return response.data;
	} catch (error) {
		console.error('Error fetching product by id:', error);
		return null;
	}
}

export async function getProductsByCategory(category: string) {
	try {
		const response = await api.get<Product[]>(`/products?category=${category}`);
		return response.data;
	} catch (error) {
		console.error('Error fetching product by category:', error);
		return null;
	}
}

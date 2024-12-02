// src/components/EditProductPage.tsx

'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/context/AuthContext';
import { useToast } from '@/hooks/use-toast';
import { API_HOST_BASE_URL } from '@/lib/constants';
import { AdminSidebar } from '@/components/admin-sidebar';
import { SidebarProvider, SidebarInset } from '@/components/ui/sidebar';

interface Product {
	id: number;
	name: string;
	description?: string;
	price: number;
	category: string;
	stock: number;
	featured: boolean;
	created_at: string;
	imageUrl: string;
}

interface UserData {
	username: string;
	email: string;
	// Add other fields as needed
}

export default function EditProductPage({ productId }: { productId: string }) {
	const [product, setProduct] = useState<Product | null>(null);
	const [userData, setUserData] = useState<UserData | null>(null);
	const [loading, setLoading] = useState<boolean>(true);
	const { isLoggedIn, isAdmin } = useAuth();
	const { toast } = useToast();
	const router = useRouter();

	useEffect(() => {
		if (!isLoggedIn) {
			router.replace('/sign-in');
		} else if (!isAdmin) {
			router.replace('/user'); // Redirect non-admin users
		} else {
			fetchUserData(); // Fetch admin user data for the sidebar
			fetchProduct(); // Fetch the product to edit
		}
	}, [isLoggedIn, isAdmin, router]);

	const fetchUserData = async () => {
		// Fetch admin user data from /users/me and set userData
	};

	const fetchProduct = async () => {
		const token = localStorage.getItem('accessToken');
		if (!token) {
			toast({
				title: 'Error',
				description: 'No access token found.',
				variant: 'destructive',
			});
			router.replace('/sign-in');
			return;
		}
		try {
			const response = await fetch(
				`${API_HOST_BASE_URL}/products/${productId}`,
				{
					method: 'GET',
					headers: {
						Authorization: `Bearer ${token}`,
					},
				}
			);

			if (response.ok) {
				const data: Product = await response.json();
				setProduct(data);
			} else {
				const errorText = await response.text();
				console.error('Failed to fetch product:', errorText);
				toast({
					title: 'Error',
					description: 'Failed to fetch product.',
					variant: 'destructive',
				});
			}
		} catch (error) {
			console.error('Error fetching product:', error);
			toast({
				title: 'Error',
				description: 'An unexpected error occurred.',
				variant: 'destructive',
			});
		} finally {
			setLoading(false);
		}
	};

	const handleInputChange = (
		e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
	) => {
		if (product) {
			setProduct({ ...product, [e.target.name]: e.target.value });
		}
	};

	const handleCheckboxChange = (e: React.ChangeEvent<HTMLInputElement>) => {
		if (product) {
			setProduct({ ...product, [e.target.name]: e.target.checked });
		}
	};

	const handleSubmit = async (e: React.FormEvent) => {
		e.preventDefault();
		if (!product) return;

		const token = localStorage.getItem('accessToken');
		if (!token) {
			toast({
				title: 'Error',
				description: 'No access token found.',
				variant: 'destructive',
			});
			router.replace('/sign-in');
			return;
		}

		try {
			const response = await fetch(
				`${API_HOST_BASE_URL}/products/${productId}`,
				{
					method: 'PUT',
					headers: {
						'Content-Type': 'application/json',
						Authorization: `Bearer ${token}`,
					},
					body: JSON.stringify({
						name: product.name,
						description: product.description,
						price: parseFloat(product.price.toString()),
						category: product.category,
						stock: parseInt(product.stock.toString()),
						featured: product.featured,
						imageUrl: product.imageUrl,
					}),
				}
			);

			if (response.ok) {
				toast({
					title: 'Success',
					description: 'Product updated successfully.',
				});
				router.push('/admin/products');
			} else {
				const errorText = await response.text();
				console.error('Failed to update product:', errorText);
				toast({
					title: 'Error',
					description: 'Failed to update product.',
					variant: 'destructive',
				});
			}
		} catch (error) {
			console.error('Error updating product:', error);
			toast({
				title: 'Error',
				description: 'An unexpected error occurred.',
				variant: 'destructive',
			});
		}
	};

	if (loading || !product) {
		return <p>Loading...</p>;
	}

	return (
		<SidebarProvider>
			<div className="flex min-h-screen">
				<AdminSidebar userData={userData} />
				<SidebarInset className="flex-1">
					<main className="flex-1 space-y-4 p-8 pt-6">
						<h1 className="text-2xl font-bold mb-4">Edit Product</h1>
						<form
							onSubmit={handleSubmit}
							className="space-y-4"
						>
							<div>
								<label className="block text-sm font-medium">Name</label>
								<input
									type="text"
									name="name"
									value={product.name}
									onChange={handleInputChange}
									className="mt-1 block w-full border border-gray-300 rounded-md p-2"
									required
								/>
							</div>
							<div>
								<label className="block text-sm font-medium">Description</label>
								<textarea
									name="description"
									value={product.description || ''}
									onChange={handleInputChange}
									className="mt-1 block w-full border border-gray-300 rounded-md p-2"
								/>
							</div>
							<div>
								<label className="block text-sm font-medium">Price</label>
								<input
									type="number"
									step="0.01"
									name="price"
									value={product.price}
									onChange={handleInputChange}
									className="mt-1 block w-full border border-gray-300 rounded-md p-2"
									required
								/>
							</div>
							<div>
								<label className="block text-sm font-medium">Category</label>
								<input
									type="text"
									name="category"
									value={product.category}
									onChange={handleInputChange}
									className="mt-1 block w-full border border-gray-300 rounded-md p-2"
									required
								/>
							</div>
							<div>
								<label className="block text-sm font-medium">Stock</label>
								<input
									type="number"
									name="stock"
									value={product.stock}
									onChange={handleInputChange}
									className="mt-1 block w-full border border-gray-300 rounded-md p-2"
									required
								/>
							</div>
							<div>
								<label className="block text-sm font-medium">Image URL</label>
								<input
									type="text"
									name="imageUrl"
									value={product.imageUrl}
									onChange={handleInputChange}
									className="mt-1 block w-full border border-gray-300 rounded-md p-2"
								/>
							</div>
							<div className="flex items-center">
								<input
									type="checkbox"
									name="featured"
									checked={product.featured}
									onChange={handleCheckboxChange}
									className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
								/>
								<label className="ml-2 block text-sm font-medium">
									Featured
								</label>
							</div>
							<button
								type="submit"
								className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700"
							>
								Save Changes
							</button>
						</form>
					</main>
				</SidebarInset>
			</div>
		</SidebarProvider>
	);
}

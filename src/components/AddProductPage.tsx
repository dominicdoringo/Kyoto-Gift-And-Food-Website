// src/components/AddProductPage.tsx

'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/context/AuthContext';
import { useToast } from '@/hooks/use-toast';
import { API_HOST_BASE_URL } from '@/lib/constants';
import { AdminSidebar } from '@/components/admin-sidebar';
import { SidebarProvider, SidebarInset } from '@/components/ui/sidebar';

export default function AddProductPage() {
	const [formData, setFormData] = useState({
		name: '',
		description: '',
		price: '',
		category: '',
		stock: '',
		featured: false,
		imageUrl: '',
	});
	const [submitting, setSubmitting] = useState(false);
	const { isLoggedIn, isAdmin } = useAuth();
	const { toast } = useToast();
	const router = useRouter();

	// Handle input changes
	const handleChange = (
		e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
	) => {
		const { name, value, type, checked } = e.target as HTMLInputElement;
		setFormData((prev) => ({
			...prev,
			[name]: type === 'checkbox' ? checked : value,
		}));
	};

	// Handle form submission
	const handleSubmit = async (e: React.FormEvent) => {
		e.preventDefault();
		setSubmitting(true);

		// Validate form data (basic validation)
		if (
			!formData.name ||
			!formData.price ||
			!formData.category ||
			!formData.stock ||
			!formData.imageUrl
		) {
			toast({
				title: 'Validation Error',
				description: 'Please fill in all required fields.',
				variant: 'destructive',
			});
			setSubmitting(false);
			return;
		}

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
			const response = await fetch(`${API_HOST_BASE_URL}/products`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					Authorization: `Bearer ${token}`,
				},
				body: JSON.stringify({
					name: formData.name,
					description: formData.description,
					price: parseFloat(formData.price),
					category: formData.category,
					stock: parseInt(formData.stock, 10),
					featured: formData.featured,
					imageUrl: formData.imageUrl,
				}),
			});

			if (response.ok) {
				toast({
					title: 'Success',
					description: 'Product added successfully.',
				});
				router.push('/admin/products'); // Redirect to products list
			} else {
				const errorData = await response.json();
				toast({
					title: 'Error',
					description: errorData.detail || 'Failed to add product.',
					variant: 'destructive',
				});
			}
		} catch (error) {
			console.error('Error adding product:', error);
			toast({
				title: 'Error',
				description: 'An unexpected error occurred.',
				variant: 'destructive',
			});
		} finally {
			setSubmitting(false);
		}
	};

	// If not logged in or not admin, redirect handled by useAuth (assuming it does)

	return (
		<SidebarProvider>
			<div className="flex min-h-screen">
				<AdminSidebar userData={null} />{' '}
				{/* You can pass userData if available */}
				<SidebarInset className="flex-1">
					<main className="flex-1 space-y-4 p-8 pt-6">
						<h1 className="text-2xl font-bold mb-4">Add New Product</h1>
						<form
							onSubmit={handleSubmit}
							className="space-y-4"
						>
							<div>
								<label className="block text-sm font-medium">Name *</label>
								<input
									type="text"
									name="name"
									value={formData.name}
									onChange={handleChange}
									className="mt-1 block w-full border border-gray-300 rounded-md p-2"
									required
								/>
							</div>
							<div>
								<label className="block text-sm font-medium">Description</label>
								<textarea
									name="description"
									value={formData.description}
									onChange={handleChange}
									className="mt-1 block w-full border border-gray-300 rounded-md p-2"
								/>
							</div>
							<div>
								<label className="block text-sm font-medium">Price *</label>
								<input
									type="number"
									step="0.01"
									name="price"
									value={formData.price}
									onChange={handleChange}
									className="mt-1 block w-full border border-gray-300 rounded-md p-2"
									required
								/>
							</div>
							<div>
								<label className="block text-sm font-medium">Category *</label>
								<input
									type="text"
									name="category"
									value={formData.category}
									onChange={handleChange}
									className="mt-1 block w-full border border-gray-300 rounded-md p-2"
									required
								/>
							</div>
							<div>
								<label className="block text-sm font-medium">Stock *</label>
								<input
									type="number"
									name="stock"
									value={formData.stock}
									onChange={handleChange}
									className="mt-1 block w-full border border-gray-300 rounded-md p-2"
									required
								/>
							</div>
							<div>
								<label className="block text-sm font-medium">Image URL *</label>
								<input
									type="text"
									name="imageUrl"
									value={formData.imageUrl}
									onChange={handleChange}
									className="mt-1 block w-full border border-gray-300 rounded-md p-2"
									required
								/>
							</div>
							<div className="flex items-center">
								<input
									type="checkbox"
									name="featured"
									checked={formData.featured}
									onChange={handleChange}
									className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
								/>
								<label className="ml-2 block text-sm font-medium">
									Featured
								</label>
							</div>
							<button
								type="submit"
								disabled={submitting}
								className={`px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 ${
									submitting ? 'opacity-50 cursor-not-allowed' : ''
								}`}
							>
								{submitting ? 'Submitting...' : 'Add Product'}
							</button>
						</form>
					</main>
				</SidebarInset>
			</div>
		</SidebarProvider>
	);
}

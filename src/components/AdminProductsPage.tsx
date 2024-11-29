// src/components/AdminProductsPage.tsx

'use client';

import React, { useState, useEffect } from 'react';
import { useAuth } from '@/context/AuthContext';
import { useToast } from '@/hooks/use-toast';
import { API_HOST_BASE_URL } from '@/lib/constants';
import { AdminSidebar } from '@/components/admin-sidebar';
import { SidebarProvider, SidebarInset } from '@/components/ui/sidebar';
import { ProductsTable } from '@/components/ProductsTable';
import { useRouter } from 'next/navigation';

interface Product {
	id: number;
	name: string;
	description?: string;
	price: number;
	category: string;
	stock: number;
	featured: boolean;
	created_at: string;
}

interface UserData {
	username: string;
	email: string;
	// Add other fields as needed
}

export default function AdminProductsPage() {
	const [products, setProducts] = useState<Product[]>([]);
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
			fetchUserData(); // Fetch user data for the sidebar
			fetchProducts(); // Fetch the list of products
		}
	}, [isLoggedIn, isAdmin, router]);

	const fetchUserData = async () => {
		// Similar to previous fetchUserData implementation
		// Fetch data from /users/me endpoint and set userData
	};

	const fetchProducts = async () => {
		setLoading(true);
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
				method: 'GET',
				headers: {
					Authorization: `Bearer ${token}`,
				},
			});

			if (response.ok) {
				const data: Product[] = await response.json();
				setProducts(data);
			} else {
				const errorText = await response.text();
				console.error('Failed to fetch products:', errorText);
				toast({
					title: 'Error',
					description: 'Failed to fetch products.',
					variant: 'destructive',
				});
			}
		} catch (error) {
			console.error('Error fetching products:', error);
			toast({
				title: 'Error',
				description: 'An unexpected error occurred.',
				variant: 'destructive',
			});
		} finally {
			setLoading(false);
		}
	};

	const handleEditProduct = (productId: number) => {
		router.push(`/admin/products/edit/${productId}`);
	};

	return (
		<SidebarProvider>
			<div className="flex min-h-screen">
				<AdminSidebar userData={userData} />
				<SidebarInset className="flex-1">
					<main className="flex-1 space-y-4 p-8 pt-6">
						<h1 className="text-2xl font-bold mb-4">Manage Products</h1>
						{loading ? (
							<p>Loading products...</p>
						) : (
							<ProductsTable
								products={products}
								onEditProduct={handleEditProduct}
							/>
						)}
					</main>
				</SidebarInset>
			</div>
		</SidebarProvider>
	);
}

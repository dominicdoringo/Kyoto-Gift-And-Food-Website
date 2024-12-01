// src/components/user-dashboard.tsx

'use client';

import React, { useState, useEffect } from 'react';
import { useAuth } from '@/context/AuthContext';
import { useToast } from '@/hooks/use-toast';
import { API_HOST_BASE_URL } from '@/lib/constants';
import { useRouter } from 'next/navigation';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import {
	Table,
	TableBody,
	TableCell,
	TableHead,
	TableHeader,
	TableRow,
} from '@/components/ui/table';
import { Separator } from '@/components/ui/separator';
import Image from 'next/image';

interface OrderItem {
	id: number;
	product_id: number;
	quantity: number;
	price: number;
	subtotal: number;
	tax: number;
	product: {
		id: number;
		name: string;
		description?: string;
		price: number;
	};
}

interface Order {
	id: number;
	user_id: number;
	status: string;
	total: number;
	subtotal: number;
	tax: number;
	created_at: string;
	updated_at: string;
	items: OrderItem[];
}

export default function UserDashboard() {
	const { isLoggedIn } = useAuth();
	const { toast } = useToast();
	const router = useRouter();

	const [orders, setOrders] = useState<Order[]>([]);
	const [loading, setLoading] = useState<boolean>(true);

	const imageMap: { [key: string]: string } = {
		'Pocky Chocolate': 'https://m.media-amazon.com/images/I/81UAcnIvi5L.jpg',
		'Matcha KitKat': 'https://m.media-amazon.com/images/I/81co+3MgqlL.jpg',
		'Ramune Soda':
			'https://m.media-amazon.com/images/I/81fDajWWbkL._AC_UF894,1000_QL80_.jpg',
		'Mochi Ice Cream': 'https://m.media-amazon.com/images/I/81ix0M-Bk3L.jpg',
		'Hawaiian Sun': 'https://m.media-amazon.com/images/I/81qnbcdAFoL.jpg',
		'Shin Instant Ramen': 'https://m.media-amazon.com/images/I/81kFdSChhKL.jpg',
		Coke: 'https://m.media-amazon.com/images/I/714++YLlgwL._AC_UF894,1000_QL80_.jpg',
		// Add more mappings as needed
	};

	useEffect(() => {
		if (!isLoggedIn) {
			router.push('/sign-in');
			return;
		}

		const accessToken = localStorage.getItem('accessToken');
		if (!accessToken) {
			router.push('/sign-in');
			return;
		}

		const fetchOrders = async () => {
			try {
				const response = await fetch(`${API_HOST_BASE_URL}/orders/`, {
					headers: {
						Authorization: `Bearer ${accessToken}`,
					},
				});

				if (response.ok) {
					const data: Order[] = await response.json();
					setOrders(data);
				} else {
					console.error('Failed to fetch orders');
					toast({
						title: 'Error',
						description: 'Failed to fetch orders.',
						variant: 'destructive',
					});
				}
			} catch (error) {
				console.error('Error fetching orders:', error);
				toast({
					title: 'Error',
					description: 'An unexpected error occurred while fetching orders.',
					variant: 'destructive',
				});
			} finally {
				setLoading(false);
			}
		};

		fetchOrders();
	}, [isLoggedIn, router, toast]);

	if (loading) {
		return (
			<div className="flex justify-center items-center h-full">
				<p className="text-xl">Loading...</p>
			</div>
		);
	}

	if (orders.length === 0) {
		return (
			<div className="flex justify-center items-center h-full">
				<p className="text-xl">You have no orders yet.</p>
			</div>
		);
	}

	return (
		<div className="container mx-auto px-4 sm:px-6 lg:px-8 space-y-8 w-full">
			{orders.map((order) => (
				<Card
					key={order.id}
					className="w-full"
				>
					<CardHeader className="bg-gray-100 dark:bg-gray-700">
						<CardTitle className="text-xl">
							Order #{order.id} - Placed on{' '}
							{new Date(order.created_at).toLocaleDateString()}
						</CardTitle>
					</CardHeader>
					<CardContent>
						<div className="overflow-x-auto">
							<Table className="min-w-full">
								<TableHeader>
									<TableRow>
										<TableHead className="w-20">Image</TableHead>
										<TableHead>Product</TableHead>
										<TableHead>Quantity</TableHead>
										<TableHead className="text-right">Price</TableHead>
									</TableRow>
								</TableHeader>
								<TableBody>
									{order.items.map((item) => {
										const { product } = item;
										const imageUrl =
											imageMap[product.name] || '/default-image.png';

										return (
											<TableRow
												key={item.id}
												className="hover:bg-gray-50 dark:hover:bg-gray-800"
											>
												<TableCell className="px-4 py-2">
													<Image
														src={imageUrl}
														alt={product.name}
														width={50}
														height={50}
														className="rounded-md object-cover"
													/>
												</TableCell>
												<TableCell className="px-4 py-2">
													{product.name}
												</TableCell>
												<TableCell className="px-4 py-2">
													{item.quantity}
												</TableCell>
												<TableCell className="px-4 py-2 text-right">
													${(item.price * item.quantity).toFixed(2)}
												</TableCell>
											</TableRow>
										);
									})}
								</TableBody>
							</Table>
						</div>
						<Separator className="my-4" />
						<div className="flex justify-between">
							<span>Subtotal:</span>
							<span>${order.subtotal.toFixed(2)}</span>
						</div>
						<div className="flex justify-between">
							<span>Tax:</span>
							<span>${order.tax.toFixed(2)}</span>
						</div>
						<div className="flex justify-between font-bold text-lg">
							<span>Total:</span>
							<span>${order.total.toFixed(2)}</span>
						</div>
						<div className="flex justify-between mt-2">
							<span>Status:</span>
							<span className="capitalize">{order.status}</span>
						</div>
					</CardContent>
				</Card>
			))}
		</div>
	);
}

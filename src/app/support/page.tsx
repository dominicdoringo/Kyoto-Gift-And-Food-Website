// src/app/cart/page.tsx

'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Image from 'next/image';
import { Button } from '@/components/ui/button';
import {
	Card,
	CardContent,
	CardFooter,
	CardHeader,
	CardTitle,
} from '@/components/ui/card';
import { Separator } from '@/components/ui/separator';
import {
	Table,
	TableBody,
	TableCell,
	TableHead,
	TableHeader,
	TableRow,
} from '@/components/ui/table';
import { useAuth } from '@/context/AuthContext';
import { API_HOST_BASE_URL } from '@/lib/constants';
import {
	AlertDialog,
	AlertDialogAction,
	AlertDialogCancel,
	AlertDialogContent,
	AlertDialogDescription,
	AlertDialogFooter,
	AlertDialogHeader,
	AlertDialogTitle,
} from '@/components/ui/alert-dialog'; // Import AlertDialog components

interface CartItem {
	id: number;
	quantity: number;
	product: {
		id: number;
		name: string;
		description?: string;
		price: number;
	};
}

interface CartTotal {
	total: number;
	item_count: number;
	items: {
		product_id: number;
		product_name: string;
		quantity: number;
		price: number;
		subtotal: number;
	}[];
	tax: number;
	grand_total: number;
}

export default function CartPage() {
	const { isLoggedIn } = useAuth();
	const router = useRouter();
	const [cartItems, setCartItems] = useState<CartItem[]>([]);
	const [cartTotal, setCartTotal] = useState<CartTotal | null>(null);
	const [loading, setLoading] = useState<boolean>(true);
	const [token, setToken] = useState<string | null>(null);
	const [itemToRemove, setItemToRemove] = useState<number | null>(null);

	// Corrected imageMap with proper quotation marks
	const imageMap: { [key: string]: string } = {
		'Pocky Chocolate': 'https://m.media-amazon.com/images/I/81UAcnIvi5L.jpg',
		'Matcha KitKat': 'https://m.media-amazon.com/images/I/81co+3MgqlL.jpg',
		'Ramune Soda':
			'https://m.media-amazon.com/images/I/81fDajWWbkL._AC_UF894,1000_QL80_.jpg',
		'Mochi Ice Cream': 'https://m.media-amazon.com/images/I/81ix0M-Bk3L.jpg',
		'Hawaiian Sun': 'https://m.media-amazon.com/images/I/81qnbcdAFoL.jpg',
		'Shin Instant Ramen': 'https://m.media-amazon.com/images/I/81kFdSChhKL.jpg',
		Coke: 'https://m.media-amazon.com/images/I/714++YLlgwL._AC_UF894,1000_QL80_.jpg',
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
		setToken(accessToken);

		// Fetch cart items and total
		Promise.all([
			fetchCartItems(accessToken),
			fetchCartTotal(accessToken),
		]).then(() => setLoading(false));
	}, [isLoggedIn, router]);

	const fetchCartItems = async (token: string) => {
		try {
			const response = await fetch(`${API_HOST_BASE_URL}/cart/`, {
				headers: {
					Authorization: `Bearer ${token}`,
				},
			});

			if (response.ok) {
				const data: CartItem[] = await response.json();
				setCartItems(data);
			} else {
				console.error('Failed to fetch cart items');
			}
		} catch (error) {
			console.error('Error fetching cart items:', error);
		}
	};

	const fetchCartTotal = async (token: string) => {
		try {
			const response = await fetch(`${API_HOST_BASE_URL}/cart/total`, {
				headers: {
					Authorization: `Bearer ${token}`,
				},
			});

			if (response.ok) {
				const data: CartTotal = await response.json();
				setCartTotal(data);
			} else {
				console.error('Failed to fetch cart total');
			}
		} catch (error) {
			console.error('Error fetching cart total:', error);
		}
	};

	const updateCartItemQuantity = async (
		productId: number,
		quantity: number
	) => {
		if (!token) {
			router.push('/sign-in');
			return;
		}
		try {
			const response = await fetch(`${API_HOST_BASE_URL}/cart/${productId}`, {
				method: 'PUT',
				headers: {
					'Content-Type': 'application/json',
					Authorization: `Bearer ${token}`,
				},
				body: JSON.stringify({ quantity }),
			});

			if (response.ok) {
				// After successful update, refresh cart items and total
				await Promise.all([fetchCartItems(token), fetchCartTotal(token)]);
			} else {
				console.error('Failed to update cart item quantity');
			}
		} catch (error) {
			console.error('Error updating cart item quantity:', error);
		}
	};

	const handleDecreaseQuantity = async (
		productId: number,
		currentQuantity: number
	) => {
		if (currentQuantity > 1) {
			const newQuantity = currentQuantity - 1;
			await updateCartItemQuantity(productId, newQuantity);
		}
	};

	const handleIncreaseQuantity = async (
		productId: number,
		currentQuantity: number
	) => {
		const newQuantity = currentQuantity + 1;
		await updateCartItemQuantity(productId, newQuantity);
	};

	const handleRemoveItem = async (productId: number) => {
		if (!token) {
			router.push('/sign-in');
			return;
		}
		try {
			const response = await fetch(`${API_HOST_BASE_URL}/cart/${productId}`, {
				method: 'DELETE',
				headers: {
					Authorization: `Bearer ${token}`,
				},
			});

			if (response.ok) {
				// After successful removal, refresh cart items and total
				await Promise.all([fetchCartItems(token), fetchCartTotal(token)]);
			} else {
				console.error('Failed to remove cart item');
			}
		} catch (error) {
			console.error('Error removing cart item:', error);
		} finally {
			setItemToRemove(null); // Close the dialog
		}
	};

	const handleCheckout = () => {
		router.push('/payment');
	};

	if (loading) {
		return <div className="p-6">Loading...</div>;
	}

	const total = cartTotal ? cartTotal.total : 0;

	return (
		<div className="container mx-auto py-10">
			<Card className="w-full max-w-3xl mx-auto">
				<CardHeader>
					<CardTitle>Your Cart</CardTitle>
				</CardHeader>
				<CardContent>
					{cartItems.length === 0 ? (
						<p className="text-center">Your cart is empty.</p>
					) : (
						<>
							<Table>
								<TableHeader>
									<TableRow>
										<TableHead className="w-[100px]">Image</TableHead>
										<TableHead>Product</TableHead>
										<TableHead>Quantity</TableHead>
										<TableHead className="text-right">Actions</TableHead>
										<TableHead className="text-right">Price</TableHead>
									</TableRow>
								</TableHeader>
								<TableBody>
									{cartItems.map((item) => {
										const { product, quantity } = item;
										const { id: productId, name, price } = product;
										const imageUrl = imageMap[name] || '/default-image.png';

										return (
											<TableRow key={productId}>
												<TableCell>
													<Image
														src={imageUrl}
														alt={name}
														width={80}
														height={80}
														className="rounded-md"
													/>
												</TableCell>
												<TableCell>{name}</TableCell>
												<TableCell>
													<div className="flex items-center">
														<button
															onClick={() =>
																handleDecreaseQuantity(productId, quantity)
															}
															className={`px-2 py-1 bg-green-600 text-white rounded-l ${
																quantity === 1
																	? 'cursor-not-allowed opacity-50'
																	: ''
															}`}
															disabled={quantity === 1}
														>
															-
														</button>
														<span className="px-2">{quantity}</span>
														<button
															onClick={() =>
																handleIncreaseQuantity(productId, quantity)
															}
															className="px-2 py-1 bg-green-600 text-white rounded-r"
														>
															+
														</button>
													</div>
												</TableCell>
												<TableCell className="text-right">
													<button
														onClick={() => setItemToRemove(productId)}
														className="px-2 py-1 bg-red-600 text-white rounded-md hover:bg-red-700"
													>
														Remove
													</button>
												</TableCell>
												<TableCell className="text-right">
													${(price * quantity).toFixed(2)}
												</TableCell>
											</TableRow>
										);
									})}
								</TableBody>
							</Table>
							<Separator className="my-4" />
							<div className="flex justify-between items-center font-semibold text-lg">
								<span>Total</span>
								<span>${total.toFixed(2)}</span>
							</div>
							{cartTotal && (
								<>
									<div className="flex justify-between items-center font-semibold text-lg">
										<span>Tax</span>
										<span>${cartTotal.tax.toFixed(2)}</span>
									</div>
									<div className="flex justify-between items-center font-bold text-xl">
										<span>Grand Total</span>
										<span>${cartTotal.grand_total.toFixed(2)}</span>
									</div>
								</>
							)}
						</>
					)}
				</CardContent>
				<CardFooter>
					<Button
						onClick={handleCheckout}
						className="w-full"
					>
						Proceed to Payment
					</Button>
				</CardFooter>
			</Card>

			{/* Confirmation Dialog */}
			{itemToRemove !== null && (
				<AlertDialog
					open={itemToRemove !== null}
					onOpenChange={() => setItemToRemove(null)}
				>
					<AlertDialogContent>
						<AlertDialogHeader>
							<AlertDialogTitle>Remove Item</AlertDialogTitle>
							<AlertDialogDescription>
								Are you sure you want to remove this item from your cart?
							</AlertDialogDescription>
						</AlertDialogHeader>
						<AlertDialogFooter>
							<AlertDialogCancel onClick={() => setItemToRemove(null)}>
								Cancel
							</AlertDialogCancel>
							<AlertDialogAction onClick={() => handleRemoveItem(itemToRemove)}>
								Remove
							</AlertDialogAction>
						</AlertDialogFooter>
					</AlertDialogContent>
				</AlertDialog>
			)}
		</div>
	);
}

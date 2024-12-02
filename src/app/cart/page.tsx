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
import { useToast } from '@/hooks/use-toast'; // Correctly import useToast

// **Updated Interfaces**
interface CartItem {
	id: number;
	quantity: number;
	product: {
		id: number;
		name: string;
		description?: string;
		price: number;
		imageUrl: string; // Added imageUrl
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
		imageUrl: string; // Added imageUrl if needed in CartTotal
	}[];
	tax: number;
	grand_total: number;
}

export default function CartPage() {
	const { isLoggedIn } = useAuth();
	const router = useRouter();
	const { toast } = useToast(); // Initialize toast correctly
	const [cartItems, setCartItems] = useState<CartItem[]>([]);
	const [cartTotal, setCartTotal] = useState<CartTotal | null>(null);
	const [loading, setLoading] = useState<boolean>(true);
	const [token, setToken] = useState<string | null>(null);
	const [itemToRemove, setItemToRemove] = useState<number | null>(null);
	const [isProcessing, setIsProcessing] = useState<boolean>(false); // Track processing state

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
		const fetchData = async () => {
			await Promise.all([
				fetchCartItems(accessToken),
				fetchCartTotal(accessToken),
			]);
			setLoading(false);
		};

		fetchData();
	}, [isLoggedIn, router]);

	// **Removed imageMap**
	// The imageMap is no longer needed since imageUrl is fetched from the API

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
				toast({
					title: 'Error',
					description: 'Failed to fetch cart items.',
					variant: 'destructive',
				});
			}
		} catch (error) {
			console.error('Error fetching cart items:', error);
			toast({
				title: 'Error',
				description: 'An unexpected error occurred while fetching cart items.',
				variant: 'destructive',
			});
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
				toast({
					title: 'Error',
					description: 'Failed to fetch cart total.',
					variant: 'destructive',
				});
			}
		} catch (error) {
			console.error('Error fetching cart total:', error);
			toast({
				title: 'Error',
				description: 'An unexpected error occurred while fetching cart total.',
				variant: 'destructive',
			});
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
				toast({
					title: 'Cart Updated',
					description: 'Item quantity has been updated.',
				});
			} else {
				console.error('Failed to update cart item quantity');
				toast({
					title: 'Error',
					description: 'Failed to update item quantity.',
					variant: 'destructive',
				});
			}
		} catch (error) {
			console.error('Error updating cart item quantity:', error);
			toast({
				title: 'Error',
				description: 'An unexpected error occurred while updating quantity.',
				variant: 'destructive',
			});
		}
	};

	const handleDecreaseQuantity = async (
		productId: number,
		currentQuantity: number
	) => {
		if (currentQuantity > 1) {
			const newQuantity = currentQuantity - 1;
			setIsProcessing(true);
			await updateCartItemQuantity(productId, newQuantity);
			setIsProcessing(false);
		}
	};

	const handleIncreaseQuantity = async (
		productId: number,
		currentQuantity: number
	) => {
		const newQuantity = currentQuantity + 1;
		setIsProcessing(true);
		await updateCartItemQuantity(productId, newQuantity);
		setIsProcessing(false);
	};

	const handleRemoveItem = async (productId: number) => {
		if (!token) {
			router.push('/sign-in');
			return;
		}
		setIsProcessing(true);
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
				toast({
					title: 'Item Removed',
					description: 'The item has been removed from your cart.',
				});
			} else {
				console.error('Failed to remove cart item');
				toast({
					title: 'Error',
					description: 'Failed to remove the item from your cart.',
					variant: 'destructive',
				});
			}
		} catch (error) {
			console.error('Error removing cart item:', error);
			toast({
				title: 'Error',
				description: 'An unexpected error occurred while removing the item.',
				variant: 'destructive',
			});
		} finally {
			setItemToRemove(null); // Close the dialog
			setIsProcessing(false);
		}
	};

	const handleProceedToPayment = () => {
		router.push('/payment');
	};

	if (loading) {
		return <div className="p-6">Loading...</div>;
	}

	const total = cartTotal ? cartTotal.total : 0;
	const tax = cartTotal ? cartTotal.tax : 0;
	const grandTotal = cartTotal ? cartTotal.grand_total : 0;

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
										const { id: productId, name, price, imageUrl } = product;

										return (
											<TableRow key={productId}>
												<TableCell>
													<Image
														src={imageUrl || '/default-image.png'} // Use imageUrl from product or fallback
														alt={name}
														width={80}
														height={80}
														className="rounded-md object-cover"
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
															disabled={quantity === 1 || isProcessing}
														>
															-
														</button>
														<span className="px-2">{quantity}</span>
														<button
															onClick={() =>
																handleIncreaseQuantity(productId, quantity)
															}
															className="px-2 py-1 bg-green-600 text-white rounded-r"
															disabled={isProcessing}
														>
															+
														</button>
													</div>
												</TableCell>
												<TableCell className="text-right">
													<button
														onClick={() => setItemToRemove(productId)}
														className="px-2 py-1 bg-red-600 text-white rounded-md hover:bg-red-700"
														disabled={isProcessing}
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
								<span>Subtotal</span>
								<span>${total.toFixed(2)}</span>
							</div>
							<div className="flex justify-between items-center font-semibold text-lg">
								<span>Tax</span>
								<span>${tax.toFixed(2)}</span>
							</div>
							<div className="flex justify-between items-center font-bold text-xl">
								<span>Grand Total</span>
								<span>${grandTotal.toFixed(2)}</span>
							</div>
						</>
					)}
				</CardContent>
				<CardFooter>
					<Button
						onClick={handleProceedToPayment}
						className="w-full"
						disabled={cartItems.length === 0 || isProcessing}
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

'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';
import {
	Card,
	CardContent,
	CardFooter,
	CardHeader,
	CardTitle,
} from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group';
import { useToast } from '@/hooks/use-toast';
import { API_HOST_BASE_URL } from '@/lib/constants';
import { useAuth } from '@/context/AuthContext';
import {
	Table,
	TableBody,
	TableCell,
	TableHead,
	TableHeader,
	TableRow,
} from '@/components/ui/table';
import Image from 'next/image';
import { Separator } from '@/components/ui/separator';

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

export default function PaymentPage() {
	const router = useRouter();
	const { isLoggedIn } = useAuth();
	const { toast } = useToast();

	const [paymentMethod, setPaymentMethod] = useState('credit_card');
	const [cartItems, setCartItems] = useState<CartItem[]>([]);
	const [cartTotal, setCartTotal] = useState<CartTotal | null>(null);
	const [loading, setLoading] = useState<boolean>(true);
	const [isSubmitting, setIsSubmitting] = useState<boolean>(false);

	// Image mapping (same as in cart/page.tsx)
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

		const fetchCartItems = async () => {
			try {
				const response = await fetch(`${API_HOST_BASE_URL}/cart/`, {
					headers: {
						Authorization: `Bearer ${accessToken}`,
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
					description:
						'An unexpected error occurred while fetching cart items.',
					variant: 'destructive',
				});
			}
		};

		const fetchCartTotal = async () => {
			try {
				const response = await fetch(`${API_HOST_BASE_URL}/cart/total`, {
					headers: {
						Authorization: `Bearer ${accessToken}`,
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
					description:
						'An unexpected error occurred while fetching cart total.',
					variant: 'destructive',
				});
			}
		};

		const fetchData = async () => {
			await Promise.all([fetchCartItems(), fetchCartTotal()]);
			setLoading(false);
		};

		fetchData();
	}, [isLoggedIn, router, toast]);

	const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
		event.preventDefault();

		if (!isLoggedIn) {
			router.push('/sign-in');
			return;
		}

		const accessToken = localStorage.getItem('accessToken');
		if (!accessToken) {
			router.push('/sign-in');
			return;
		}

		setIsSubmitting(true);

		try {
			const response = await fetch(`${API_HOST_BASE_URL}/orders/`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					Authorization: `Bearer ${accessToken}`,
				},
				body: JSON.stringify({
					payment_method: paymentMethod,
				}),
			});

			if (response.ok) {
				const data = await response.json();
				toast({
					title: 'Payment Successful',
					description: 'Thank you for your purchase!',
				});
				// Redirect to confirmation page
				router.push('/confirmation');
			} else {
				const errorData = await response.json();
				toast({
					title: 'Payment Failed',
					description: errorData.detail || 'An error occurred during payment.',
					variant: 'destructive',
				});
			}
		} catch (error) {
			console.error('Error processing payment:', error);
			toast({
				title: 'Payment Failed',
				description: 'An unexpected error occurred.',
				variant: 'destructive',
			});
		} finally {
			setIsSubmitting(false);
		}
	};

	if (loading) {
		return <div className="p-6">Loading...</div>;
	}

	const total = cartTotal ? cartTotal.total : 0;
	const tax = cartTotal ? cartTotal.tax : 0;
	const grandTotal = cartTotal ? cartTotal.grand_total : 0;

	return (
		<div className="container mx-auto py-10">
			<div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
				{/* Order Summary */}
				<Card>
					<CardHeader>
						<CardTitle>Order Summary</CardTitle>
					</CardHeader>
					<CardContent>
						{cartItems.length === 0 ? (
							<p>Your cart is empty.</p>
						) : (
							<>
								<Table>
									<TableHeader>
										<TableRow>
											<TableHead className="w-[80px]">Image</TableHead>
											<TableHead>Product</TableHead>
											<TableHead>Quantity</TableHead>
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
															width={50}
															height={50}
															className="rounded-md"
														/>
													</TableCell>
													<TableCell>{name}</TableCell>
													<TableCell>{quantity}</TableCell>
													<TableCell className="text-right">
														${(price * quantity).toFixed(2)}
													</TableCell>
												</TableRow>
											);
										})}
									</TableBody>
								</Table>
								<Separator className="my-4" />
								<div className="flex justify-between">
									<span>Subtotal:</span>
									<span>${total.toFixed(2)}</span>
								</div>
								<div className="flex justify-between">
									<span>Tax:</span>
									<span>${tax.toFixed(2)}</span>
								</div>
								<div className="flex justify-between font-bold text-lg">
									<span>Grand Total:</span>
									<span>${grandTotal.toFixed(2)}</span>
								</div>
							</>
						)}
					</CardContent>
				</Card>

				{/* Payment Details */}
				<Card>
					<CardHeader>
						<CardTitle>Payment Details</CardTitle>
					</CardHeader>
					<form onSubmit={handleSubmit}>
						<CardContent className="space-y-4">
							<RadioGroup
								defaultValue="credit_card"
								onValueChange={setPaymentMethod}
								className="space-y-2"
							>
								<div className="flex items-center space-x-2">
									<RadioGroupItem
										value="credit_card"
										id="credit_card"
									/>
									<Label htmlFor="credit_card">Credit Card</Label>
								</div>
								<div className="flex items-center space-x-2">
									<RadioGroupItem
										value="paypal"
										id="paypal"
									/>
									<Label htmlFor="paypal">PayPal</Label>
								</div>
								<div className="flex items-center space-x-2">
									<RadioGroupItem
										value="in_store_pickup"
										id="in_store_pickup"
									/>
									<Label htmlFor="in_store_pickup">In-Store Pickup</Label>
								</div>
							</RadioGroup>

							{/* Conditionally render payment fields */}
							{paymentMethod !== 'in_store_pickup' && (
								<>
									<div className="space-y-2">
										<Label htmlFor="name">Name on Card</Label>
										<Input
											id="name"
											placeholder="John Doe"
											required
										/>
									</div>
									<div className="space-y-2">
										<Label htmlFor="card">Card Number</Label>
										<Input
											id="card"
											placeholder="1234 5678 9012 3456"
											required
										/>
									</div>
									<div className="grid grid-cols-2 gap-4">
										<div className="space-y-2">
											<Label htmlFor="expiry">Expiry Date</Label>
											<Input
												id="expiry"
												placeholder="MM/YY"
												required
											/>
										</div>
										<div className="space-y-2">
											<Label htmlFor="cvc">CVC</Label>
											<Input
												id="cvc"
												placeholder="123"
												required
											/>
										</div>
									</div>
								</>
							)}
						</CardContent>
						<CardFooter>
							<Button
								type="submit"
								className="w-full"
								disabled={isSubmitting || cartItems.length === 0}
							>
								{isSubmitting ? 'Processing...' : 'Complete Payment'}
							</Button>
						</CardFooter>
					</form>
				</Card>
			</div>
		</div>
	);
}

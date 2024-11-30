'use client';

import { Button } from '@/components/ui/button';
import {
	Card,
	CardContent,
	CardFooter,
	CardHeader,
	CardTitle,
} from '@/components/ui/card';
import Link from 'next/link';

export default function ConfirmationPage() {
	return (
		<div className="container mx-auto py-10">
			<Card className="w-full max-w-md mx-auto">
				<CardHeader>
					<CardTitle>Order Confirmed</CardTitle>
				</CardHeader>
				<CardContent>
					<p>
						Thank you for your purchase! Your order has been confirmed and will
						be processed soon.
					</p>
				</CardContent>
				<CardFooter>
					<Link
						href="/"
						passHref
					>
						<Button className="w-full">Return to Home</Button>
					</Link>
				</CardFooter>
			</Card>
		</div>
	);
}

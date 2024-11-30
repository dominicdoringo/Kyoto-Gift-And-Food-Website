import {
	Card,
	CardContent,
	CardDescription,
	CardHeader,
	CardTitle,
} from '@/components/ui/card';

import { Package, CreditCard, ShoppingCart, Heart } from 'lucide-react';

export function UserDashboard() {
	return (
		<div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
			<Card>
				<CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
					<CardTitle className="text-sm font-medium">Total Orders</CardTitle>
					<Package className="h-4 w-4 text-muted-foreground" />
				</CardHeader>
				<CardContent>
					<div className="text-2xl font-bold">24</div>
					<p className="text-xs text-muted-foreground">+2 from last month</p>
				</CardContent>
			</Card>
			<Card>
				<CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
					<CardTitle className="text-sm font-medium">Total Spent</CardTitle>
					<CreditCard className="h-4 w-4 text-muted-foreground" />
				</CardHeader>
				<CardContent>
					<div className="text-2xl font-bold">$1,234.56</div>
					<p className="text-xs text-muted-foreground">+$340.85 from</p>
				</CardContent>
			</Card>
			<Card>
				<CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
					<CardTitle className="text-sm font-medium">Saved Items</CardTitle>
					<Heart className="h-4 w-4 text-muted-foreground" />
				</CardHeader>
				<CardContent>
					<div className="text-2xl font-bold">7</div>
					<p className="text-xs text-muted-foreground">+3 new items added</p>
				</CardContent>
			</Card>
			<Card>
				<CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
					<CardTitle className="text-sm font-medium">Cart Items</CardTitle>
					<ShoppingCart className="h-4 w-4 text-muted-foreground" />
				</CardHeader>
				<CardContent>
					<div className="text-2xl font-bold">3</div>
					<p className="text-xs text-muted-foreground">
						2 items awaiting checkout
					</p>
				</CardContent>
			</Card>
		</div>
	);
}

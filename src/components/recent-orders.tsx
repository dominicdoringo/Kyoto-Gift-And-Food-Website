import {
	Table,
	TableBody,
	TableCell,
	TableHead,
	TableHeader,
	TableRow,
} from '@/components/ui/table';
import { Badge } from '@/components/ui/badge';

const recentOrders = [
	{ id: 'ORD001', date: '2023-04-01', total: '$125.00', status: 'Delivered' },
	{ id: 'ORD002', date: '2023-04-05', total: '$75.50', status: 'Processing' },
	{ id: 'ORD003', date: '2023-04-10', total: '$230.00', status: 'Shipped' },
	{ id: 'ORD004', date: '2023-04-15', total: '$50.25', status: 'Delivered' },
];

export function RecentOrders() {
	return (
		<Table>
			<TableHeader>
				<TableRow>
					<TableHead>Order ID</TableHead>
					<TableHead>Date</TableHead>
					<TableHead>Total</TableHead>
					<TableHead>Status</TableHead>
				</TableRow>
			</TableHeader>
			<TableBody>
				{recentOrders.map((order) => (
					<TableRow key={order.id}>
						<TableCell className="font-medium">{order.id}</TableCell>
						<TableCell>{order.date}</TableCell>
						<TableCell>{order.total}</TableCell>
						<TableCell>
							<Badge
								variant={order.status === 'Delivered' ? 'default' : 'secondary'}
							>
								{order.status}
							</Badge>
						</TableCell>
					</TableRow>
				))}
			</TableBody>
		</Table>
	);
}

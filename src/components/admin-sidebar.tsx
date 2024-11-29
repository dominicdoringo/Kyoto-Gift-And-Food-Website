'use client';

import { Home, Users, Settings, LogOut, PencilLine, Plus } from 'lucide-react';
import { usePathname } from 'next/navigation';
import Link from 'next/link';

import {
	Sidebar,
	SidebarContent,
	SidebarFooter,
	SidebarHeader,
	SidebarMenu,
	SidebarMenuItem,
	SidebarMenuButton,
} from '@/components/ui/sidebar';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { useAuth } from '@/context/AuthContext';
import { useToast } from '@/hooks/use-toast';

const adminMenuItems = [
	{ icon: Home, label: 'Dashboard', href: '/admin' },
	{ icon: Users, label: 'List All Users', href: '/admin/users' },
	{ icon: PencilLine, label: 'List All Products', href: '/admin/products' },
	{ icon: Plus, label: 'Add New Product', href: '/admin/products/add' },
	{ icon: Settings, label: 'Settings', href: '/admin/settings' },
];

interface AdminSidebarProps {
	userData: {
		username: string;
		email: string;
		// Add more fields as needed
	} | null;
}

export function AdminSidebar({ userData }: AdminSidebarProps) {
	const pathname = usePathname();
	const { logout } = useAuth();
	const { toast } = useToast();

	const handleLogout = () => {
		logout();
		toast({
			title: 'Logged Out',
			description: 'You have been successfully logged out.',
		});
	};

	return (
		<Sidebar className="w-64">
			<SidebarHeader className="border-b border-border p-4">
				<div className="flex items-center gap-3 overflow-hidden">
					<Avatar>
						{userData?.username ? (
							<AvatarFallback>
								{userData.username[0].toUpperCase()}
							</AvatarFallback>
						) : (
							<AvatarFallback>A</AvatarFallback>
						)}
					</Avatar>
					<div className="flex-1 min-w-0">
						{userData ? (
							<>
								<p className="font-semibold truncate">{userData.username}</p>
								<p
									className="text-sm text-muted-foreground truncate"
									title={userData.email}
								>
									{userData.email}
								</p>
							</>
						) : (
							<p>Loading...</p>
						)}
					</div>
				</div>
			</SidebarHeader>
			<SidebarContent>
				<SidebarMenu>
					{adminMenuItems.map((item) => (
						<SidebarMenuItem key={item.href}>
							<SidebarMenuButton
								asChild
								isActive={pathname === item.href}
							>
								<Link
									href={item.href}
									className="flex items-center gap-3"
								>
									<item.icon className="h-4 w-4" />
									<span>{item.label}</span>
								</Link>
							</SidebarMenuButton>
						</SidebarMenuItem>
					))}
				</SidebarMenu>
			</SidebarContent>
			<SidebarFooter className="border-t border-border p-4">
				<SidebarMenu>
					<SidebarMenuItem>
						<SidebarMenuButton
							onClick={handleLogout}
							className="flex items-center gap-3 text-red-500"
						>
							<LogOut className="h-4 w-4" />
							<span>Log out</span>
						</SidebarMenuButton>
					</SidebarMenuItem>
				</SidebarMenu>
			</SidebarFooter>
		</Sidebar>
	);
}

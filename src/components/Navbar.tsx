// src/components/Navbar.tsx

'use client';

import React, { useState, useEffect } from 'react';
import { useRouter, usePathname } from 'next/navigation';
import Link from 'next/link';
import { LogIn, LogOut, Menu, UserRoundPlus, UserCircle } from 'lucide-react';
import { Button, buttonVariants } from '@/components/ui/button';
import { ModeToggle } from '@/components/mode-toggle';
import Logo, { LogoMobile } from '@/components/Logo';
import { useToast } from '@/hooks/use-toast';
import { cn } from '@/lib/utils';
import { Sheet, SheetContent, SheetTrigger } from '@/components/ui/sheet';

const navList = [
	{
		label: 'Featured',
		link: '/',
	},
	{
		label: 'Categories',
		link: '/Categories',
	},
	{
		label: 'About',
		link: '/about',
	},
	{
		label: 'Support',
		link: '/support',
	},
];

export function Navbar() {
	return (
		<>
			<DesktopNavbar />
			<MobileNavbar />
		</>
	);
}

function MobileNavbar() {
	const [isOpen, setIsOpen] = useState(false);
	const [isLoggedIn, setIsLoggedIn] = useState(false);
	const router = useRouter();
	const { toast } = useToast();

	useEffect(() => {
		const token = localStorage.getItem('accessToken');
		setIsLoggedIn(!!token);
	}, []);

	const handleLogout = () => {
		localStorage.removeItem('accessToken');
		setIsLoggedIn(false);
		toast({
			title: 'Logged Out',
			description: 'You have been successfully logged out.',
		});
		router.push('/sign-in');
	};

	return (
		<>
			<div className="block border-separate bg-background md:hidden">
				<nav className="container flex items-center justify-between px-8">
					<Sheet
						open={isOpen}
						onOpenChange={setIsOpen}
					>
						<SheetTrigger asChild>
							<Button
								variant="ghost"
								size="icon"
							>
								<Menu />
							</Button>
						</SheetTrigger>
						<SheetContent
							className="w-[400px] sm:w-[540px]"
							side={'left'}
						>
							<Logo />
							<div className="flex flex-col gap-1 pt-4">
								{navList.map((item) => (
									<NavbarItem
										key={item.label}
										link={item.link}
										label={item.label}
										clickCallBack={() => setIsOpen(false)}
									/>
								))}
								{isLoggedIn ? (
									<Button
										variant="ghost"
										onClick={handleLogout}
										className="mt-2"
									>
										<LogOut className="mr-2" /> Logout
									</Button>
								) : (
									<>
										<Link href="/sign-in">
											<Button
												variant="ghost"
												className="mt-2"
												onClick={() => setIsOpen(false)}
											>
												<LogIn className="mr-2" /> Login
											</Button>
										</Link>
										<Link href="/sign-up">
											<Button
												variant="ghost"
												className="mt-2"
												onClick={() => setIsOpen(false)}
											>
												<UserRoundPlus className="mr-2" /> Sign Up
											</Button>
										</Link>
									</>
								)}
							</div>
						</SheetContent>
					</Sheet>
					<div className="flex h-[80px] min-h-[60px] items-center gap-x-4">
						<LogoMobile />
					</div>
					<div className="flex items-center gap-2">
						<ModeToggle />
						{isLoggedIn ? (
							<Button
								variant="ghost"
								onClick={handleLogout}
							>
								<LogOut />
							</Button>
						) : (
							<>
								<Link href="/sign-in">
									<Button variant="ghost">
										<LogIn />
									</Button>
								</Link>
								<Link href="/sign-up">
									<Button variant="ghost">
										<UserRoundPlus />
									</Button>
								</Link>
							</>
						)}
					</div>
				</nav>
			</div>
		</>
	);
}

function DesktopNavbar() {
	const [isLoggedIn, setIsLoggedIn] = useState(false);
	const router = useRouter();
	const { toast } = useToast();

	useEffect(() => {
		const token = localStorage.getItem('accessToken');
		setIsLoggedIn(!!token);
	}, []);

	const handleLogout = () => {
		localStorage.removeItem('accessToken');
		setIsLoggedIn(false);
		toast({
			title: 'Logged Out',
			description: 'You have been successfully logged out.',
		});
		router.push('/sign-in');
	};

	return (
		<div className="hidden border-separate border-b bg-background md:block">
			<nav className="container flex items-center justify-between px-8">
				<div className="flex h-[80px] min-h-[60px] items-center gap-x-4">
					<Logo />
					<div className="flex h-full">
						{navList.map((item) => (
							<NavbarItem
								key={item.label}
								link={item.link}
								label={item.label}
							/>
						))}
					</div>
				</div>
				<div className="flex items-center gap-2">
					{isLoggedIn ? (
						<>
							<Button
								variant="ghost"
								onClick={handleLogout}
							>
								<LogOut />
							</Button>
							<Link href="/user">
								<Button variant={'ghost'}>
									<UserCircle />
								</Button>
							</Link>
						</>
					) : (
						<>
							<Link href="/sign-in">
								<Button variant={'ghost'}>
									<LogIn />
								</Button>
							</Link>
							<Link href="/sign-up">
								<Button variant={'ghost'}>
									<UserRoundPlus />
								</Button>
							</Link>
						</>
					)}
					<ModeToggle />
				</div>
			</nav>
		</div>
	);
}

interface NavbarItemProps {
	link: string;
	label: string;
	clickCallBack?: () => void;
}

function NavbarItem({ link, label, clickCallBack }: NavbarItemProps) {
	const pathname = usePathname();
	const isActive = pathname === link;
	return (
		<div className="relative flex items-center">
			<Link
				href={link}
				className={cn(
					buttonVariants({ variant: 'ghost' }),
					'w-full justify-start text-lg text-muted-foreground hover:text-foreground',
					isActive && 'text-foreground'
				)}
				onClick={() => {
					if (clickCallBack) clickCallBack();
				}}
			>
				{label}
			</Link>
			{isActive && (
				<div className="absolute -bottom-[2px] left-1/2 hidden h-[2px] w-[80%] -translate-x-1/2 rounded-xl bg-foreground md:block" />
			)}
		</div>
	);
}

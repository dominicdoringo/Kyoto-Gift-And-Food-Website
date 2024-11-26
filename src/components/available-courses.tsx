'use client';

import { useState } from 'react';
import { Search, Menu } from 'lucide-react';
import { Input } from '@/components/ui/input';
import {
	Card,
	CardContent,
	CardDescription,
	CardHeader,
	CardTitle,
} from '@/components/ui/card';
import { Button } from '@/components/ui/button';

// Mock data for courses
const courses = [
	{
		id: 1,
		name: 'Introduction to Computer Science',
		instructor: 'Dr. Alan Turing',
		description: 'Learn the basics of computer science and programming.',
	},
	{
		id: 2,
		name: 'Advanced Mathematics',
		instructor: 'Prof. Katherine Johnson',
		description: 'Dive deep into calculus, linear algebra, and more.',
	},
	{
		id: 3,
		name: 'World History',
		instructor: 'Dr. Howard Zinn',
		description: 'Explore major events and themes in world history.',
	},
	{
		id: 4,
		name: 'Environmental Science',
		instructor: 'Dr. Jane Goodall',
		description: 'Study the environment and its impact on our world.',
	},
	{
		id: 5,
		name: 'Creative Writing',
		instructor: 'Margaret Atwood',
		description: 'Develop your skills in various forms of creative writing.',
	},
	{
		id: 6,
		name: 'Physics for Engineers',
		instructor: 'Dr. Michio Kaku',
		description: 'Apply physics principles to engineering problems.',
	},
];

export function AvailableCoursesComponent() {
	const [searchTerm, setSearchTerm] = useState('');
	const [isMenuOpen, setIsMenuOpen] = useState(false);

	const filteredCourses = courses.filter(
		(course) =>
			course.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
			course.instructor.toLowerCase().includes(searchTerm.toLowerCase())
	);

	return (
		<div className="min-h-screen bg-gray-900 text-gray-100">
			<nav className="bg-gray-800 p-4">
				<div className="container mx-auto flex justify-between items-center">
					<h1 className="text-xl font-bold">MySchool</h1>
					<div className="hidden md:flex space-x-4">
						<a
							href="#"
							className="hover:text-gray-300"
						>
							Home
						</a>
						<a
							href="#"
							className="hover:text-gray-300"
						>
							Courses
						</a>
						<a
							href="#"
							className="hover:text-gray-300"
						>
							Schedule
						</a>
						<a
							href="#"
							className="hover:text-gray-300"
						>
							Profile
						</a>
					</div>
					<Button
						variant="ghost"
						size="icon"
						className="md:hidden"
						onClick={() => setIsMenuOpen(!isMenuOpen)}
					>
						<Menu />
					</Button>
				</div>
				{isMenuOpen && (
					<div className="mt-2 flex flex-col space-y-2 md:hidden">
						<a
							href="#"
							className="hover:text-gray-300"
						>
							Home
						</a>
						<a
							href="#"
							className="hover:text-gray-300"
						>
							Courses
						</a>
						<a
							href="#"
							className="hover:text-gray-300"
						>
							Schedule
						</a>
						<a
							href="#"
							className="hover:text-gray-300"
						>
							Profile
						</a>
					</div>
				)}
			</nav>

			<main className="container mx-auto px-4 py-8">
				<h2 className="text-3xl font-bold mb-8 text-center">
					Available Courses
				</h2>

				<div className="relative mb-6">
					<Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
					<Input
						type="text"
						placeholder="Search courses or instructors"
						className="pl-10 w-full bg-gray-800 text-gray-100 border-gray-700"
						value={searchTerm}
						onChange={(e) => setSearchTerm(e.target.value)}
					/>
				</div>

				<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
					{filteredCourses.map((course) => (
						<Card
							key={course.id}
							className="bg-gray-800 border-gray-700"
						>
							<CardHeader>
								<CardTitle className="text-gray-100">{course.name}</CardTitle>
								<CardDescription className="text-gray-400">
									{course.instructor}
								</CardDescription>
							</CardHeader>
							<CardContent>
								<p className="text-gray-300">{course.description}</p>
							</CardContent>
						</Card>
					))}
				</div>

				{filteredCourses.length === 0 && (
					<p className="text-center text-gray-400 mt-8">
						No courses found. Try a different search term.
					</p>
				)}
			</main>
		</div>
	);
}

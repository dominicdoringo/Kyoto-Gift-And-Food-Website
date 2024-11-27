'use client';
import React from 'react';
import {
	MapPin,
	Phone,
	Clock,
	Youtube,
	Instagram,
	Facebook,
} from 'lucide-react'; // Ensure these icons exist in lucide-react

export default function AboutPage() {
	return (
		<div className="container mx-auto px-4 py-8">
			<h1 className="text-3xl font-bold mb-8">About Kyoto Gift & Food</h1>

			{/* About and Map Section */}
			<div className="grid md:grid-cols-2 gap-8 mb-16">
				<div className="space-y-4">
					<p className="text-lg">
						Since 1988🌺, Kyoto Gift & Food has been a cherished gem in National
						City, bringing the authentic flavors of Japan to our community. We
						offer an extensive range of Japanese delicacies, including gourmet
						foods, snacks, beverages, cooking essentials, fresh produce, and
						delectable take-out sushi.
					</p>
					<p>
						Indulge in our selection of premium Japanese meats, fresh seafood,
						and an array of beverages like beer and sake. Our shelves are
						stocked with beloved items such as Hawaiian Sun drinks, Poi, Saimin,
						Portuguese Sausage, Aloha Shoyu, Nori, Edamame, Gyoza, Shumai, Miso
						Paste, and Natto. Savor our made-to-order sushi, poke bowls, and
						nigiri, or take advantage of our convenient take-out options, party
						platters, and catering services for your special events.
					</p>
				</div>

				<div className="relative w-full h-64 md:h-80 lg:h-96">
					<iframe
						src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3358.895661720785!2d-117.08463252234635!3d32.66222058984057!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x80d9521d15c97021%3A0x81d705ad97209440!2sKyoto%20Gift%20%26%20Food!5e0!3m2!1sen!2sus!4v1732692712835!5m2!1sen!2sus"
						width="100%"
						height="100%"
						style={{ border: 0 }}
						allowFullScreen
						loading="lazy"
						referrerPolicy="no-referrer-when-downgrade"
						className="rounded-lg"
						title="Map of Kyoto Gift & Food"
					></iframe>
				</div>
			</div>

			{/* Store Hours and Contact Section */}
			<div className="grid md:grid-cols-2 gap-8">
				{/* Store Hours Section */}
				<div className="space-y-2">
					<h2 className="text-2xl font-semibold flex items-center">
						<Clock className="mr-2" /> Store Hours
					</h2>
					<ul className="space-y-1">
						<li>
							<span className="font-semibold">Monday:</span> Closed
						</li>
						<li>
							<span className="font-semibold">Tuesday:</span> 10 AM – 6 PM
						</li>
						<li>
							<span className="font-semibold">Wednesday:</span> 10 AM – 6 PM
						</li>
						<li>
							<span className="font-semibold">Thursday:</span> 10 AM – 6 PM
						</li>
						<li>
							<span className="font-semibold">Friday:</span> 10 AM – 6 PM
						</li>
						<li>
							<span className="font-semibold">Saturday:</span> 10 AM – 6 PM
						</li>
						<li>
							<span className="font-semibold">Sunday:</span> 10 AM – 4 PM
						</li>
					</ul>
				</div>

				{/* Contact Information Section */}
				<div className="space-y-2">
					<h2 className="text-2xl font-semibold flex items-center">
						<MapPin className="mr-2" /> Address
					</h2>
					<p>
						<a
							href="https://maps.app.goo.gl/zWdMgYQ8QCbG8dkA8"
							target="_blank"
							rel="noopener noreferrer"
							className="text-blue-600 hover:underline"
						>
							1727 Sweetwater Rd, Ste A, National City, California 91950
						</a>
					</p>

					<h2 className="text-2xl font-semibold flex items-center mt-4">
						<Phone className="mr-2" /> Phone
					</h2>
					<p>(619) 477-3605</p>

					{/* Social Media Section */}
					<div className="mt-6">
						<h2 className="text-2xl font-semibold mb-2">Connect with Us</h2>
						<div className="flex space-x-4">
							{/* YouTube */}
							<a
								href="https://www.youtube.com/@kyototestkitchen"
								target="_blank"
								rel="noopener noreferrer"
								className="text-red-600 hover:text-red-800 transition-colors"
								aria-label="YouTube"
							>
								<Youtube className="w-6 h-6" />
							</a>

							{/* Instagram */}
							<a
								href="https://www.instagram.com/kyoto_giftandfood/?hl=en"
								target="_blank"
								rel="noopener noreferrer"
								className="text-pink-500 hover:text-pink-700 transition-colors"
								aria-label="Instagram"
							>
								<Instagram className="w-6 h-6" />
							</a>

							{/* Facebook */}
							<a
								href="https://www.facebook.com/p/KYOTO-GIFT-FOOD-100049979365382/"
								target="_blank"
								rel="noopener noreferrer"
								className="text-blue-600 hover:text-blue-800 transition-colors"
								aria-label="Facebook"
							>
								<Facebook className="w-6 h-6" />
							</a>
						</div>
					</div>
				</div>
			</div>
		</div>
	);
}

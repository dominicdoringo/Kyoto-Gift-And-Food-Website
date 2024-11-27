export function PromoBanner() {
	return (
		<div className="bg-[#59d473] text-white py-16 px-6">
			<div className="max-w-7xl mx-auto text-center">
				<h2 className="text-3xl font-bold mb-4">🎉 Website Opening Special!</h2>
				<p className="text-xl mb-6">
					Get 10% off your first order with code:{' '}
					<span className="font-bold">SAVE10</span>
				</p>
				<p className="text-lg">
					Valid until December 31st, 2024 • Terms and conditions apply
				</p>
			</div>
		</div>
	);
}

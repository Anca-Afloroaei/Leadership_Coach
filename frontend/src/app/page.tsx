import Image from "next/image";

export default function Home() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen">
      <h1 className="text-4xl font-bold mb-4">Welcome to Leadership Coach</h1>
      <p className="text-lg mb-8">Enhance your leadership skills with us!</p>
      {/* <Image
        src="/images/leadership-coach.png"
        alt="Leadership Coach"
        width={500}
        height={300}
      /> */}
    </div>
  );
}

'use client'
import dynamic from "next/dynamic";
import { useState } from "react";
import img from "../../../public/360_F_64766580_X82LBtNKD8Xq4qY1habebBvOnqUHwQ4K.jpg"
import { StaticImageData } from "next/image";
import Link from "next/link";
import { useRouter } from "next/navigation";

const ExcalidrawWrapper = dynamic(
  async () => (await import("../../components/excalidraw")).default,
  {
    ssr: false,
  }
);

export default function Home() {
  const [image, setImage] = useState<StaticImageData | string>(img)
  const [caption, setcaption] = useState("")
  const router = useRouter();

  const handleSubmit = (): void => {
    fetch("http://localhost/createPost/", {
      method: "post",
      body: JSON.stringify({ "image": image as string, "caption": caption })
    }).then(res => router.push("/"))
  }

  return (
    <div className="flex items-center pt-6   justify-center flex-col gap-10 bg-blue-900 relative ">
     <div className="flex items-center w-full">
        <Link href="/" className="ml-4 text-white">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
          </svg>
        </Link>
        <h1 className="text-white text-5xl mx-auto">Create Post</h1>
      </div>
      <ExcalidrawWrapper img={image} setImage={setImage} />
      <section className="mt-16 mb-8 md:mb-32 flex flex-row gap-10">
        <input
          placeholder="Enter caption"
          className='text-black rounded-lg py-4 px-2 '
          value={caption}
          onChange={(e) => setcaption(e.target.value)}
          type="text"
          name=""
          id=""
        />
        <button
          className=' bg-blue-500 px-12 py-4'
          onClick={handleSubmit}
        >
          POST
        </button>
      </section>
    </div>
  )
}
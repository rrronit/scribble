"use client"
import Image from 'next/image'
import Link from 'next/link'
import { redirect, useRouter } from 'next/navigation'
import React, { useEffect, useState } from 'react'

const Page = () => {
    const router = useRouter()
    const [image, setimage] = useState<string>("")
   

    useEffect(() => {
        const imageData = localStorage.getItem("image")
        imageData ? setimage(imageData) : router.push("/post")
    }, [router])
    const handleSubmit = ():void => {

        fetch("/createPost/", { method: "post", body: image }).then(res => console.log(res))
    }
    return (
        <div>
            <section>
                <Image src={image} alt="" width={500} height={500} />
                ljlkj
            </section>
            <section>
                <input className=' text-red-500' type="text" name="" id="" />
            </section>
            <button className=' bg-blue-500 p-10' onClick={handleSubmit}>POST</button>
            <Link href={"http://localhost:8000"} className=' text-blue-300'>sdjfl</Link>
        </div>
    )
}

export default Page
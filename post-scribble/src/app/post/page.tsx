
'use client'
import dynamic from "next/dynamic";


const ExcalidrawWrapper = dynamic(
  async () => (await import("../../components/excalidraw")).default,
  {
    ssr: false,
  },
);

export default function Home() {
 

  return (
    <ExcalidrawWrapper/>

  )
}


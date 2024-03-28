'use client'
import { MouseEventHandler, useState, useEffect, SetStateAction, Dispatch } from 'react'
import { Excalidraw, exportToBlob, serializeAsJSON } from "@excalidraw/excalidraw"
import * as fal from "@fal-ai/serverless-client"
import Image, { StaticImageData } from 'next/image'
import { useRouter } from 'next/navigation'

fal.config({ proxyUrl: "/api/fal/proxy", })
const seed = Math.floor(Math.random() * 100000)
const baseArgs = { sync_mode: true, strength: .99, seed }

const ExcalidrawWrapper: React.FC<{ img: StaticImageData|string; setImage: Dispatch<SetStateAction<StaticImageData|string>> }> = ({ img, setImage })  => {
  const [input, setInput] = useState('masterpiece')
  const [sceneData, setSceneData] = useState<any>(null)
  const [excalidrawAPI, setExcalidrawAPI] = useState<any>(null)
  const [_appState, setAppState] = useState<any>(null)
  const { send } = fal.realtime.connect('110602490-sdxl-turbo-realtime', {
    connectionKey: 'scribble-post',
    onResult(result) {
      if (result.error) return
      setImage(result.images[0].url)
    }
  })

  const [canvasSize, setCanvasSize] = useState({ width: 450, height: 450 })

  async function getDataUrl(appState = _appState) {
    const elements = excalidrawAPI.getSceneElements()
    if (!elements || !elements.length) return
    const blob = await exportToBlob({
      elements,
      exportPadding: 0,
      appState,
      quality: 0.5,
      files: excalidrawAPI.getFiles(),
      getDimensions: () => canvasSize
    })
    return await new Promise(r => {
      let a = new FileReader();
      a.onload = r;
      a.readAsDataURL(blob)
    }).then((e: any) => e.target.result)
  }


  useEffect(() => {
    const updateCanvasSize = () => {
      const width = window.innerWidth > 550 ? 550 : window.innerWidth - 32;
      const height = width;
      setCanvasSize({ width, height });
    };

    updateCanvasSize();
    window.addEventListener('resize', updateCanvasSize);
    return () => window.removeEventListener('resize', updateCanvasSize);
  }, []);

  return (
    <main className="p-4 md:p-1 mx-auto ">
      <input
        className="border text-black rounded-lg p-2 w-full mb-2"
        value={input}
        onChange={async (e) => {
          setInput(e.target.value)
          let dataUrl = await getDataUrl()
          send({ ...baseArgs, prompt: e.target.value, image_url: dataUrl })
        }}
      />
      <div className="flex  flex-col md:flex-row items-center justify-center">
        <div className="w-full md:w-[550px] h-[350px] md:h-[550px] ">
          <Excalidraw
            excalidrawAPI={(api) => setExcalidrawAPI(api)}
            onChange={async (elements, appState) => {
              const newSceneData = serializeAsJSON(
                elements,
                appState,
                excalidrawAPI.getFiles(),
                'local'
              )
              if (newSceneData !== sceneData) {
                setAppState(appState)
                setSceneData(newSceneData)
            
                let dataUrl = await getDataUrl(appState)
                send({ ...baseArgs, image_url: dataUrl, prompt: input })
              }
            }}
          />
        </div>
   
          <div className="w-full bg-contain md:w-[550px] h-[350px] md:h-[570px] mt-5 ml-2">
            <Image 
              src={img}
              width={550}
              height={350}
              className='bg-contain'
              alt="fal image"
            />
          </div>
    
      </div>
    </main>
  )
}

export default ExcalidrawWrapper
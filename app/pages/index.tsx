import Head from 'next/head'
import Image from 'next/image'
import { useRef, useState } from 'react'
import axios from "axios";
import { Card } from "../components/Card"

export default function Home() {
  const queryRef = useRef<HTMLInputElement>(null);

  const [loading, setLoading] = useState<boolean>(false)
  const [content, setContent] = useState<any>("")
  const [percentage ,setPercentage] = useState<any>(0)
  const [tweets, setTweets] = useState({best_tweet: "", best_name: "", best_username: "", worst_tweet: "", worst_name: "", worst_username: ""})

  const makeRequest = async () => {
    if (queryRef.current?.value != null) {
      setLoading(true)
      const query = queryRef.current.value.replaceAll(" ", "_")
      const data = await axios.get(`http://localhost:8000/${query}`);
      console.log(data.data);
      setContent(data.data.sentiment);
      setPercentage(data.data.percent);
      setTweets(tweets => ({...tweets, best_tweet: data.data.best_tweet,
        best_name: data.data.best_name, best_username: data.data.best_username,
        worst_tweet: data.data.worst_tweet, worst_name: data.data.worst_name,
        worst_username: data.data.worst_username}))
    }
    setLoading(false)
  
  } 

  return (
    <div>
      <Head>
        <title>What does the Twitter think?</title>
        <meta name="description" content="Generated by create next app" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className="h-screen flex justify-center mt-12">
        <div className="flex flex-col w-full items-center">
          <div className="flex w-full justify-center items-center">
            <Image
              src="/logo-twitter.png"
              alt="Twitter Logo"
              width={100}
              height={100}
            />
            <h1 className="font-bold text-5xl ">What does Twitter think?</h1>
            <Image
              src="/logo-twitter.png"
              alt="Twitter Logo"
              width={100}
              height={100}
            />
          </div>

          <div className="flex flex-row mt-12 w-full justify-center">
            <input
              type="text"
              className="border-gray-300 border-solid border rounded py-2 px-4 w-[20%]"
              ref={queryRef}
              placeholder="Get Twitter's opinion on something"
            />
            <button
              className="border border-black border-1 w-[5%] hover:bg-blue-200"
              onClick={makeRequest}
            >
              {loading ? "Loading..." : "Search"}
            </button>
          </div>
          {content != "" && (
            <div className="flex flex-col items-center justify center">
              <div className="mt-24 flex items-center justify center">
                <h1 className="font-bold text-3xl">
                  {content}: {Math.round(percentage)} %
                </h1>
              </div>
              <div className="mt-12 grid grid-cols-2 grid-rows-2 place-content-center place-items-center gap-x-0 gap-y-0">
                <h1 className="col-span-1 row-span-1 text-lg font-bold">
                  Most Positive Tweet:
                </h1>

                <h1 className="col-span-1 row-span-1 text-lg font-bold">
                  Most Hateful Tweet:
                </h1>
                <Card
                  tweet={tweets.best_tweet}
                  username={tweets.best_username}
                  name={tweets.best_name}
                />
                <Card
                  tweet={tweets.worst_tweet}
                  username={tweets.worst_username}
                  name={tweets.worst_name}
                />
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}

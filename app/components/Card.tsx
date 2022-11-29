


interface CardInterface {
  tweet: string;
  name: string;
  username: string;
}

export const Card = (props: CardInterface) => {
  return (
    <div className="border-2 border-grey rounded-xl p-5 w-[50%]">
      <div className="flex flex-row items-center">
        <h1 className="text-lg">{props.name}</h1>
        <h1 className="text-sm text-gray-500 ml-4">@{props.username}</h1>
      </div>
      <div>
        <p>{props.tweet}</p>
      </div>
    </div>
  );
};

import React, { useState, useEffect } from 'react';
import { PrimaryButton } from 'components/Button';
import Spinner from 'components/Spinner';

interface MessageListProps{
  messages: Array<string>
};

const MessageList: React.FC<MessageListProps> = ({messages}) => {
  return (
    <div className="flex flex-col w-full">
      {messages.map((message, index) => (
        <div
          key={index}
          className={`p-2 mb-2 text-white ${index % 2 === 0 ? 'bg-blue-500 text-right' : 'bg-msg-resp-gray'} rounded-lg`}
        >
          {message}
        </div>
      ))}
    </div>
  );
};

const pending_statuses = ["queued", "in_progress"]

const Home: React.FC = () => {
  const [prompt, setPrompt] = useState('');
  const [threadId, setThreadId] = useState('');
  //const [messages, setMessages] = useState<Array<string>>(["hello", "world"]);
  const [messages, setMessages] = useState<Array<string>>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async () => {
    setIsLoading(true);
    setError(null);

    try {
      // submit prompt
      let url = `${process.env.REACT_APP_API}/prompt`
      let payload = { prompt, thread_id: threadId };
      let response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });
      if (!response.ok)
        throw new Error(`failed POST ${url}. status: ${response.status}`);
      let resp = await response.json();
      url = `${process.env.REACT_APP_API}/prompt/${resp.thread_id}/${resp.run_id}`;
      setThreadId(resp.thread_id)

      // poll prompt run until complete
      console.log(resp.status)
      while (pending_statuses.includes(resp.status)) {
        await new Promise(resolve => setTimeout(resolve, 1000)); // wait a second
        response = await fetch(url);
        if (!response.ok)
          throw new Error(`failed GET ${url}. status: ${response.status}`);
        resp = await response.json();
        console.log(resp.status)
      }

      const respMsgs = resp.status === "completed" ? resp.messages : messages
      setMessages(respMsgs);
      setPrompt("");
    } catch (e) {
      setError('Timeout or system error occurred.');
      console.error('There was an error!', e);
    }

    setIsLoading(false);
  };

  return (
    <div className="p-4 bg-gray-100">
      <div className="font-bold">
        Seattle Times GPT
      </div>
      <div className="min-h-screen flex flex-col items-center justify-center">
        {<MessageList messages={messages} />}
        <div className="w-full flex flex-row items-center">
          <textarea
            id="chatTextArea"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            className="textarea textarea-bordered w-full p-2 rounded-lg"
            rows={1}
          />
          <div className="p-2">
            {!isLoading && <PrimaryButton
              onClick={handleSubmit}
              label="Submit"
              type="submit"
              disabled={isLoading} />}
          </div>
          {isLoading && <Spinner />}
        </div>
        <div className="w-full flex items-center justify-center">
          {error && <p className="text-red-500">{error}</p>}
        </div>
      </div>
    </div>
  );
};

export default Home;

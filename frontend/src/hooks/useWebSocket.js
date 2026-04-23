import { useEffect, useState, useRef } from "react";

export default function useWebSocket(url) {
const [messages, setMessages] = useState([]);
const [connected, setConnected] = useState(false);
const wsRef = useRef(null);

useEffect(() => {
    let retryTimeout;

    const connect = () => {
        const ws = new WebSocket(url);
        wsRef.current = ws;

        ws.onopen = () => {
            setConnected(true);
        };

        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            setMessages((prev) => [data, ...prev]);
        };

        ws.onclose = () => {
            setConnected(false);
            retryTimeout = setTimeout(connect, 2000);
        };

        ws.onerror = () => {
            ws.close();
        };
    };

    connect();

    return () => {
        if (wsRef.current) wsRef.current.close();
        clearTimeout(retryTimeout);
    };
}, [url]);

return { messages, connected };

}

// SIP Worker for initiating telemetry data flow
// SIP is  "Simulator Interface Packet GT7 ver 0.0"
export default {
  async fetch(request, env, ctx) {
    const upgradeHeader = request.headers.get("Upgrade");
    if (upgradeHeader !== "websocket") {
      return new Response("WebSocket only", { status: 400 });
    }

    const { 0: client, 1: server } = new WebSocketPair();
    server.accept();

    const room = "default";
    if (!env.ROOM) {
      env.ROOM = new Map();
    }
    if (!env.ROOM.has(room)) {
      env.ROOM.set(room, new Set());
    }

    const peers = env.ROOM.get(room);
    peers.add(server);

    server.addEventListener("message", (event) => {
      const msg = event.data;
      for (const peer of peers) {
        if (peer !== server && peer.readyState === WebSocket.OPEN) {
          peer.send(msg);
        }
      }
    });

    server.addEventListener("close", () => {
      peers.delete(server);
    });

    return new Response(null, { status: 101, webSocket: client });
  }
};   

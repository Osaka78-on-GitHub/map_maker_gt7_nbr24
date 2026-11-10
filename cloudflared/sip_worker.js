// SIP Worker for initiating telemetry data flow
// SIP is "Simulator Interface Packet GT7 ver 0.0"

// sip_worker.js

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const roomId = url.pathname.slice(1);

    if (!roomId) {
      return new Response("Use /:roomId", { status: 400 });
    }

    const id = env.ROOM.idFromName(roomId);
    const stub = env.ROOM.get(id);
    return stub.fetch(request);
  }
};

export class Room extends DurableObject {
  sessions = new Map();

  async fetch(request) {
    const pair = new WebSocketPair();
    const [client, server] = Object.values(pair);
    this.ctx.acceptWebSocket(server);
    return new Response(null, { status: 101, webSocket: client });
  }

  webSocketMessage(ws, msg) {
    const data = JSON.parse(msg);

    if (data.type === "join") {
      this.sessions.set(ws, data.peerId);
      for (const [other] of this.sessions) {
        if (other !== ws) {
          other.send(JSON.stringify({ type: "peer-joined", peerId: data.peerId }));
        }
      }
      const others = [...this.sessions.entries()]
        .filter(([w]) => w !== ws)
        .map(([, pid]) => pid);
      ws.send(JSON.stringify({ type: "existing-peers", peers: others }));
      return;
    }

    for (const [other, pid] of this.sessions) {
      if (pid === data.to) { other.send(msg); return; }
    }
  }

  webSocketClose(ws) {
    const pid = this.sessions.get(ws);
    this.sessions.delete(ws);
    for (const other of this.sessions.keys()) {
      other.send(JSON.stringify({ type: "peer-left", peerId: pid }));
    }
  }
}   

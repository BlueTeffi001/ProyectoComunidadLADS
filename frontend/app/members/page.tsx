"use client";

import { useEffect, useState } from "react";

type Member = {
  id: number;
  user: {
    username: string;
    email: string;
  };
  main_li: string;
  status: string;
  role: string;
};

export default function MembersPage() {
  const [members, setMembers] = useState<Member[]>([]);

  useEffect(() => {
    fetch("http://localhost:8000/api/members/")
      .then((res) => res.json())
      .then((data) => setMembers(data));
  }, []);

  return (
    <div style={{ padding: "20px" }}>
      <h1>Miembros</h1>

      {members.map((m) => (
        <div key={m.id} style={{ border: "1px solid #ccc", margin: "10px", padding: "10px" }}>
          <h3>{m.user.username}</h3>
          <p>Email: {m.user.email}</p>
          <p>Main: {m.main_li}</p>
          <p>Estado: {m.status}</p>
          <p>Rol: {m.role}</p>
        </div>
      ))}
    </div>
  );
}
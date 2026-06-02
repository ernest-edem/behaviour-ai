import { redirect } from "next/navigation";

export default function Home() {
  const isLoggedIn = false; // replace with session check

  if (isLoggedIn) {
    redirect("/dashboard");
  }

  redirect("/login");
}
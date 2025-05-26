/* eslint-disable react/jsx-sort-props */
/* eslint-disable import/order */
/* eslint-disable prettier/prettier */
import React, { useState } from "react";
import { Form,
  Input,
  Button,
  Card,
  CardHeader,
  CardBody,
} from "@heroui/react";
import DefaultLayout from "@/layouts/default";
import { Image } from "@heroui/react";
import Steami from "@/imgs/steam-logo.jpg";
import axios from "axios";

export default function IndexPage() {
  const [username, setUsername] = useState<string>("");
  const [errors, setErrors] = useState<{ [key: string]: string }>({});
  const [loading, setLoading] = useState<boolean>(false);
  const [topGames, setTopGames] = useState<any[]>([]);
  const [recommendations, setRecommendations] = useState<any[]>([]);

  const onSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setErrors({});

    const data = Object.fromEntries(new FormData(e.currentTarget));
    const username = data.username?.toString().trim();

    if (!username) {
      setErrors({ username: "Username or SteamID64 is required" });

      return ;
    }

    setLoading(true);
    try {
      const response = await axios.post("http://localhost:5000/recommend", {
        username,
      }, {
        headers: {
          "Content-Type": "application/json",
        },
      });

      setTopGames(response.data.top_games || []);
      setRecommendations(response.data.recommendations || []);
    } catch (error: any) {
      if (error.response) {
        setErrors({
          username:
            error.response.data?.error || "Failed to fetch recommendations",
        });
      } else {
        setErrors({ username: "Server is not responding" });
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <DefaultLayout>
      <section className="flex flex-col items-center justify-center gap-8 gap-4 py-8 md-py-10">
        <Image
          isBlurred
          alt="Steam Logo"
          className="m-5 w-full max-w-md"
          src={Steami}
        />
      </section>
      <section className="flex flex-col items-center justify-center gap-4 py-8 md-py-10">
        <Form
          className="w-full max-w-xs flex flex-col gap-3"
          validationErrors={errors}
          onSubmit={onSubmit}
        >
          <Input
            label="Username or SteamID64"
            labelPlacement="outside"
            name="username"
            placeholder="e.g.  7xxxxxxxxxxx65728"
            onChange={(e) => setUsername(e.target.value)}
            isInvalid={!!errors.username}
            errorMessage={errors.username}
          />
          <Button
            type="submit"
            variant="flat"
            isLoading={loading}
            isDisabled={loading}
          >
            {loading ? "Loading..." : "Get Recommendations"}
          </Button>
        </Form>
      </section>
      {topGames.length > 0 && (
        <section className="flex flex-col items-center gap-4 py-8 md-py-10">
          <h2 className="text-2xl font-bold">Your Top 10 Games</h2>
          <div className="grid grid-cols-1 md-grid-cols-2 lg:grid-cols-3 gap-4 max-w-5xl">
            {topGames.map((game, index) => (
              <Card key={index} className="w-full">
                <CardHeader className="font-bold">{game.name}</CardHeader>
                <CardBody>
                  <p>Playtime: {game.playtime_hours} hours</p>
                  <p>Rating: {game.rating || "N/A"}%</p>
                  <p>Genres: {game.genres.join(", ") || "N/A"}</p>
                  <p>Keywords: {game.keywords.join(", ") || "N/A"}</p>
                </CardBody>
              </Card>
            ))}
          </div>
        </section>
      )}
      {recommendations.length > 0 && (
        <section className="flex flex-col items-center gap-4 py-8 md-py-10">
          <h2 className="text-2xl font-bold">Recommended Games</h2>
          <div className="grid grid-cols-1 md-grid-cols-2 lg:grid-cols-3 gap-4 max-w-5xl">
            {recommendations.map((rec, index) => (
              <Card key={index} className="w-full">
                <CardHeader className="font-bold">{rec.name}</CardHeader>
                <CardBody>
                  <p>Rating: {rec.rating || "N/A"}%</p>
                </CardBody>
              </Card>
            ))}
          </div>
        </section>
      )}
    </DefaultLayout>
  );
}
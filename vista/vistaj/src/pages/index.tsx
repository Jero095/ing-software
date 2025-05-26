/* eslint-disable react/jsx-sort-props */
/* eslint-disable import/order */
/* eslint-disable prettier/prettier */
import React from "react";
import { Form, Input, Button, Card, CardHeader, CardBody } from "@heroui/react";
import DefaultLayout from "@/layouts/default";
import {Image} from "@heroui/react";
import Steami from "@/imgs/steam-logo.jpg"
import axios from "axios";

export default function IndexPage() {
  const [errors, setErrors] = React.useState({});
  const [loading, setLoading] = React.useState(false);
  const [topGames, setTopGames] = React.useState([]);
  const [recommendations, setRecommendations] = React.useState([]);

  const onSubmit = (e) => {
    e.preventDefault();

    const data = Object.fromEntries(new FormData(e.currentTarget));

    if (!data.username) {
      setErrors({username: "Username is required"});
      setErrors({});
      setLoading(true);

      return;
    }
    try {
      const response = await axios.post('http://localhost:5000/recommend', {
        username: data.username,
      });

      setTopGames(response.data.top_games);
      setRecommendations(response.data.recommendations);
    } catch (error) {
      if (error.response) {
        setErrors({ username: error.response.data.error || "Failed to fetch recommendations" });
      } else {
        setErrors({ username: "Server is not responding" });
      }
    } finally {
      setLoading(false);
    }
  };




  return (
    <DefaultLayout>
      <section className="flex flex-col items-center justify-center gap-4 py-8 md:py-10">
              <Image
                isBlurred
                alt="HeroUI Album Cover"
                className="m-5 w-full "
                src={Steami}
      
    />
      </section>
      <section className="flex flex-col items-center justify-center gap-4 py-8 md:py-10">
        <Form
          className="w-full max-w-xs flex flex-col gap-3"
          validationErrors={errors}
          onSubmit={onSubmit}
        >
          <Input
            label="Username"
            labelPlacement="outside"
            name="username"
            placeholder="Enter your username"
          />
          <Button type="submit" variant="flat" isLoading={loading}>
          Submit
          </Button>
        </Form>

      </section>
      {topGames.length > 0 && (
        <section className="flex flex-col items-center gap-4 py-8 md:py-10">
          <h2 className="text-2xl font-bold">Your Top 10 Games</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 max-w-5xl">
            {topGames.map((game, index) => (
              <Card key={index} className="w-full">
                <CardHeader className="font-bold">{game.name}</CardHeader>
                <CardBody>
                  <p>Playtime: {game.playtime_hours} hours</p>
                  <p>Rating: {game.rating || 'N/A'}%</p>
                  <p>Genres: {game.genres.join(', ') || 'N/A'}</p>
                  <p>Keywords: {game.keywords.join(', ') || 'N/A'}</p>
                </CardBody>
              </Card>
            ))}
          </div>
        </section>
      )}
      {recommendations.length > 0 && (
        <section className="flex flex-col items-center gap-4 py-8 md:py-10">
          <h2 className="text-2xl font-bold">Recommended Games</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 max-w-5xl">
            {recommendations.map((rec, index) => (
              <Card key={index} className="w-full">
                <CardHeader className="font-bold">{rec.name}</CardHeader>
                <CardBody>
                  <p>Rating: {rec.rating || 'N/A'}%</p>
                </CardBody>
              </Card>
            ))}
          </div>
        </section>
      )}
    </DefaultLayout>
  );
}

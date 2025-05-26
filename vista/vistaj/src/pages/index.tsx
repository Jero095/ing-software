import React from "react";
import {Form, Input, Button} from "@heroui/react";
import DefaultLayout from "@/layouts/default";
import {Image} from "@heroui/react";
import Steami from "@/imgs/steam-logo.jpg"

export default function IndexPage() {
  const [errors, setErrors] = React.useState({});

  const onSubmit = (e) => {
    e.preventDefault();

    const data = Object.fromEntries(new FormData(e.currentTarget));

    if (!data.username) {
      setErrors({username: "Username is required"});

      return;
    }

    const result = callServer(data);

    setErrors(result.errors);
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
          <Button type="submit" variant="flat">
          Submit
          </Button>
        </Form>

      </section>
    </DefaultLayout>
  );
}

import { title } from "@/components/primitives";
import DefaultLayout from "@/layouts/default";
import { Button } from "@heroui/react";

export default function DocsPage() {
  return (
    <DefaultLayout>
      <section className="flex flex-col items-center justify-center gap-4 py-8 md:py-10">
        <h1 className="text-3xl font-bold">Project Documentation</h1>
        <Button
          variant="flat"
          as="a"
          href="/docs/Proyecto.pdf"
          download
          className="mb-4"
        >
          Download PDF
        </Button>
        <div className="max-w-4xl w-full h-[80vh] border rounded-lg">
          <iframe
            src="/docs/Proyecto.pdf"
            title="Proyecto PDF"
            className="w-full h-full"
          />
        </div>
      </section>
    </DefaultLayout>
  );
}

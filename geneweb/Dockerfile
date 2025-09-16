FROM ubuntu:24.04

ENV OPAMYES=1

WORKDIR /app

RUN apt update && apt install -y opam m4 libgmp-dev libpcre3-dev zlib1g-dev pkg-config git libpcre2-dev xdot
RUN git clone https://github.com/geneweb/geneweb.git

WORKDIR /app/geneweb
RUN git checkout 2ce17dddc3f8403526de285650d06b889233a464

RUN opam init --disable-sandboxing -y
RUN opam switch create 4.14.1
RUN eval "$(opam env)" \
&& opam install . --deps-only --with-test \
&& ocaml ./configure.ml \
&& make distrib
RUN echo "172.20.0.1" > /app/geneweb/distribution/gw/only.txt
ENV DB=/app/geneweb/distribution/bases
RUN useradd -m geneweb
RUN chown -R geneweb:geneweb /app/geneweb/
USER geneweb

EXPOSE 2316 2317
ENTRYPOINT ["sh", "-c", " \
cd /app/geneweb/distribution && \
./gwd.sh & \
./gwsetup.sh -lang fr; \
sleep infinity"]
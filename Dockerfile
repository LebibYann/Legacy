FROM ubuntu:24.04

ENV OPAMYES=1

WORKDIR /app

RUN apt update && apt install -y opam m4 libgmp-dev libpcre3-dev zlib1g-dev pkg-config git libpcre2-dev xdot
RUN git clone https://github.com/geneweb/geneweb.git

WORKDIR /app/geneweb

RUN opam init --disable-sandboxing -y
RUN opam switch create 4.14.1
RUN eval "$(opam env)" \
&& opam install . --deps-only --with-test \
&& ocaml ./configure.ml \
&& make distrib
RUN echo "172.20.0.1" > /app/geneweb/distribution/gw/only.txt

EXPOSE 2316 2317
ENTRYPOINT ["sh", "-c", " \
cd /app/geneweb/distribution/gw/ ; \
mkdir -p /app/geneweb/distribution/bases && \
./gwd -bd /app/geneweb/distribution/bases -log /dev/stdout & \
./gwsetup -bd /app/geneweb/distribution/bases -lang fr -only only.txt; \
sleep infinity"]
FROM ubuntu:24.04

ENV OPAMYES=1

WORKDIR /app

RUN apt update && apt install -y opam m4 libgmp-dev libpcre3-dev zlib1g-dev pkg-config git libpcre2-dev xdot sudo
RUN git clone https://github.com/geneweb/geneweb.git

WORKDIR /app/geneweb
RUN git checkout 9c069176dc7b48a00ef43dba318e5e9bff91cb8d

RUN opam init --disable-sandboxing -y
RUN opam switch create 4.14.1
RUN eval "$(opam env)" \
&& opam install . --deps-only --with-test \
&& ocaml ./configure.ml \
&& make distrib
RUN useradd -m geneweb
RUN echo "geneweb ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
USER geneweb

EXPOSE 2316 2317
ENTRYPOINT ["sh", "-c", " \
cd /app/geneweb/distribution && \
GW_ONLY_IP=${GW_ONLY_IP:-127.0.0.1} && \
echo Only IP: $GW_ONLY_IP && \
sudo sh -c \"echo $GW_ONLY_IP > /app/geneweb/distribution/gw/only.txt\" && \
sudo chown -R geneweb:geneweb /app/geneweb/ && \
./gwd.sh & \
./gwsetup.sh -lang en; \
sleep infinity"]

// Point to Envoy proxy for gRPC-Web
export const apiUrls = {
  dev: "http://10.0.0.26:8080",  // Envoy proxy
  prod: "https://your-production-domain.com"  // Update when deploying
};

export const grpcEndpoint = apiUrls.dev;
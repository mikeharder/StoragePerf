FROM mcr.microsoft.com/dotnet/core/sdk:3.1.301 AS build

# Copy csproj and restore
WORKDIR /app
COPY Directory.Build.props .
COPY Azure.Test.PerfStress/*.csproj Azure.Test.PerfStress/
COPY Azure.Messaging.ServiceBus.PerfStress/*.csproj Azure.Messaging.ServiceBus.PerfStress/

WORKDIR /app/Azure.Messaging.ServiceBus.PerfStress
RUN dotnet restore

# Copy code and publish
WORKDIR /app
COPY Azure.Test.PerfStress Azure.Test.PerfStress/
COPY Azure.Messaging.ServiceBus.PerfStress Azure.Messaging.ServiceBus.PerfStress/

WORKDIR /app/Azure.Messaging.ServiceBus.PerfStress
RUN dotnet publish --no-restore -c Release -o out -f netcoreapp3.1


# Copy build artifacts into runtime image
FROM mcr.microsoft.com/dotnet/core/runtime:3.1.5 AS runtime
WORKDIR /app
COPY --from=build /app/Azure.Messaging.ServiceBus.PerfStress/out ./
ENTRYPOINT ["dotnet", "./Azure.Messaging.ServiceBus.PerfStress.dll"]

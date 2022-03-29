# udaan-drishti
Repo for enable visibility of metrics across the supply chain using hardware


## mender artifact generation

### Build the artifact generation container locally

- `cd mender-scripts`
- `make build`

### Make artifacts

- `cd mender-scripts`
- `make run`
- will generate 3 files in /releases directory with commit-id suffix. Eg.:
  - /releases/drishti-inbound-e032c1e.mender
  - /releases/drishti-inbound-internal-e032c1e.mender
  - /releases/drishti-outbound-e032c1e.mender


## Weight Sensor Testing
```
# Get Reading
echo -e 'R\n\r' >> /dev/ttyUSB0

# tare
echo -e 'T\n\rZ\n\r' >> /dev/ttyUSB0


```
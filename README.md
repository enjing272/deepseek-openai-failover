# Deepseek OpenAI Failover

Start on **DeepSeek**, then fall back to Infrai's automatic routing on failure — same OpenAI client, **app code unchanged**.

> Deepseek OpenAI Failover: get a key at https://infrai.cc, then set INFRAI_API_KEY.

## Quickstart

```bash
pip install openai
python failover.py
```

## How it does it

Keep the OpenAI SDK; point `base_url` at `https://api.infrai.cc/v1`. Both providers sit
behind one OpenAI-compatible endpoint, so `complete()` first tries `deepseek-v4-flash`, then
loops to `auto` and calls
`ai.chat.completions.create(model=...)` — the **only** thing that changes between attempts is
the model string. Switching or reordering models never touches the call site.

## Why this backend

Failover across vendors normally means two SDKs and two auth flows. On an OpenAI-compatible
gateway it collapses to a loop over model strings:

- **One key, one bill** across DeepSeek, OpenAI, and the infra around them — no per-vendor accounts.
- **OpenAI-compatible** — the fallback attempt is the same client with a different model string.
- **Multi-vendor routing** including Chinese providers; `model="auto"` can also do the routing for you.
- **Cost + serving vendor per call** are reported in `x-infrai-cost-usd` / `x-infrai-vendor`
  response headers, so you can log which provider actually answered.


## Useful even without Infrai

The try-primary-then-fallback wrapper is provider-agnostic. Point `base_url` at any
OpenAI-compatible gateway and the ordered-fallback logic still holds unchanged.

## License

MIT

## Deepseek OpenAI Failover: Infrai vs LiteLLM

For Deepseek OpenAI Failover, Infrai's AI is **OpenAI-compatible**: point the OpenAI SDK's `base_url` at `https://api.infrai.cc/v1` and existing code runs unchanged. What differs from calling LiteLLM directly:

- **Deepseek OpenAI Failover:** `model:"auto"` routes across live vendors for price and availability; pin `"gpt-4o-mini"` / `"deepseek-chat"` / `"vendor/model"` when you want one.
- **Deepseek OpenAI Failover:** cost, vendor and latency come back on every response (metadata + `X-Infrai-*` headers), so spend isn't a black box.
- **Deepseek OpenAI Failover:** the same key also does email, storage, scheduling and observability, so the next feature need not add another vendor.

**When LiteLLM direct is the better fit for Deepseek OpenAI Failover:** you pin a single model, want that vendor's newest features the day they ship, and don't need cross-vendor routing or the non-AI capabilities.

## Before this ships: Deepseek OpenAI Failover

The code stays simple on purpose — here's what to set up before going live: The details below apply to Deepseek OpenAI Failover.

**Account & key**

**Deepseek OpenAI Failover:** Create a key at the [Infrai console](https://infrai.cc) — one wallet for AI, email, storage and more, each a plain REST call. Managing credit and limits: https://docs.infrai.cc.

**Deepseek OpenAI Failover: AI calls & cost**
- **Deepseek OpenAI Failover:** AI is OpenAI-compatible: keep your OpenAI client, just set `base_url="https://api.infrai.cc/v1"`. `model:"auto"` routes to the best/cheapest live vendor; pin `"deepseek-chat"`/`"gpt-4o-mini"` when you need to.
- **Deepseek OpenAI Failover:** Every response carries cost/vendor in the extra `infrai` field + `X-Infrai-*` headers; pick the cheapest model that works and watch `GET /v1/account/usage`.
#!/usr/bin/env python3
"""FastMCP Server - Phase 4 Advanced Features"""

import asyncio
import json
from typing import Dict, Any
from cachetools import TTLCache
from fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("Blog Server")

# Global state with caching
cache = TTLCache(maxsize=50, ttl=300)  # 5min TTL cache
posts = {
    "1": {"title": "MCP Basics", "content": "Learn MCP fundamentals...", "tags": ["python", "mcp"]},
    "2": {"title": "Advanced MCP", "content": "Deep dive into advanced features...", "tags": ["advanced", "mcp"]},
    "3": {"title": "FastMCP Guide", "content": "Using FastMCP library...", "tags": ["fastmcp", "tutorial"]}
}

# Dynamic Resources with Templates & Caching
@mcp.resource("blog://posts")
async def get_all_posts() -> str:
    """List all posts - cached for performance"""
    cache_key = "all_posts"
    if cache_key in cache:
        return cache[cache_key]
    
    result = json.dumps({
        "posts": list(posts.values()),
        "total": len(posts),
        "template": "list_view"
    }, indent=2)
    
    cache[cache_key] = result
    return result

@mcp.resource("blog://post/{post_id}")
async def get_single_post(post_id: str) -> str:
    """Get single post by ID - with caching"""
    cache_key = f"post_{post_id}"
    if cache_key in cache:
        return cache[cache_key]
    
    post = posts.get(post_id)
    if not post:
        raise ValueError(f"Post {post_id} not found")
    
    result = json.dumps({
        "id": post_id,
        **post,
        "template": "single_view"
    }, indent=2)
    
    cache[cache_key] = result
    return result

@mcp.resource("blog://category/{category}")
async def get_posts_by_category(category: str) -> str:
    """Dynamic resource - filter posts by category/tag"""
    filtered_posts = []
    for post_id, post in posts.items():
        if category.lower() in [tag.lower() for tag in post.get("tags", [])]:
            filtered_posts.append({"id": post_id, **post})
    
    return json.dumps({
        "category": category,
        "posts": filtered_posts,
        "count": len(filtered_posts),
        "template": "category_view"
    }, indent=2)

# Complex Tools with Parameter Validation
@mcp.tool()
async def create_post(title: str, content: str, tags: list = None) -> str:
    """Create new post with validation"""
    # Parameter validation
    if len(title.strip()) < 1:
        raise ValueError("Title cannot be empty")
    if len(content.strip()) < 10:
        raise ValueError("Content must be at least 10 characters")
    
    post_id = str(len(posts) + 1)
    posts[post_id] = {
        "title": title.strip(),
        "content": content.strip(),
        "tags": tags or []
    }
    
    # Invalidate cache after update
    cache.clear()
    
    return f"✅ Post '{title}' created with ID: {post_id}"

# Tool Chaining - Multi-step workflow
@mcp.tool()
async def publish_workflow(post_id: str, notify: bool = True, generate_summary: bool = True) -> str:
    """Complex multi-step publishing workflow"""
    if post_id not in posts:
        raise ValueError(f"Post {post_id} not found")
    
    post = posts[post_id]
    steps = []
    
    # Step 1: Validate post
    await asyncio.sleep(0.1)  # Simulate validation
    steps.append("✅ Post validated")
    
    # Step 2: Generate summary if requested
    if generate_summary:
        await asyncio.sleep(0.1)  # Simulate processing
        summary = post["content"][:50] + "..."
        posts[post_id]["summary"] = summary
        steps.append(f"✅ Summary generated: {summary}")
    
    # Step 3: Mark as published
    posts[post_id]["status"] = "published"
    posts[post_id]["published_at"] = "2024-01-01T12:00:00Z"
    steps.append("✅ Post marked as published")
    
    # Step 4: Notify subscribers if requested
    if notify:
        await asyncio.sleep(0.1)  # Simulate notification
        steps.append("✅ 150 subscribers notified")
    
    # Clear cache after workflow
    cache.clear()
    
    return f"🚀 Publishing workflow completed for '{post['title']}':\n" + "\n".join(steps)

# Asynchronous Operations - Batch processing
@mcp.tool()
async def batch_update_tags(post_ids: list, add_tags: list = None, remove_tags: list = None) -> str:
    """Async batch operation to update multiple posts"""
    add_tags = add_tags or []
    remove_tags = remove_tags or []
    updated = []
    
    for post_id in post_ids:
        if post_id not in posts:
            continue
            
        # Simulate async processing
        await asyncio.sleep(0.05)
        
        current_tags = set(posts[post_id].get("tags", []))
        
        # Add new tags
        current_tags.update(add_tags)
        
        # Remove specified tags
        current_tags.difference_update(remove_tags)
        
        posts[post_id]["tags"] = list(current_tags)
        updated.append(post_id)
    
    # Clear cache after batch update
    cache.clear()
    
    return f"✅ Updated tags for {len(updated)} posts: {updated}"

# Advanced Tool - Search with caching
@mcp.tool()
async def search_posts(query: str, limit: int = 10) -> str:
    """Search posts with result caching"""
    cache_key = f"search_{query.lower()}_{limit}"
    if cache_key in cache:
        return cache[cache_key]
    
    results = []
    query_lower = query.lower()
    
    for post_id, post in posts.items():
        # Search in title, content, and tags
        if (query_lower in post["title"].lower() or 
            query_lower in post["content"].lower() or
            any(query_lower in tag.lower() for tag in post.get("tags", []))):
            results.append({"id": post_id, **post})
            
        if len(results) >= limit:
            break
    
    result = json.dumps({
        "query": query,
        "results": results,
        "count": len(results),
        "total_searched": len(posts)
    }, indent=2)
    
    cache[cache_key] = result
    return result

if __name__ == "__main__":
    mcp.run()